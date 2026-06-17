"""Read-side model: parse tool notes and category files, search examples, list.

A tool note (tool-notes/<tool>.md) holds curated shell examples grouped under
"## Use case" headings, inside ```bash code fences. Each example line is a
command optionally followed by an inline "# intent" comment. find() searches
those; list_categories() reads the doc/categories/*.md tier.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .roots import Root

# Fences whose contents are reusable shell (indexable by find).
_INDEXABLE_FENCES = {"", "bash", "sh", "shell", "zsh", "console"}

# A category bullet:  - [display](../../tool-notes/slug.md) — description
_BULLET_RE = re.compile(r"^- \[(?P<display>[^\]]*)\]\((?P<target>[^)]*)\)(?:\s+—\s+(?P<desc>.*))?$")
# Inline intent: first run of whitespace followed by '#'.
_INTENT_RE = re.compile(r"[ \t]+#")


@dataclass(frozen=True)
class ToolRef:
    slug: str  # tool-note filename stem (the id used by open/find/add)
    display: str  # link text shown in the category file
    desc: str


@dataclass
class Category:
    name: str  # H1 of the category file
    slug: str  # filename stem (kebab)
    file: Path
    tools: list[ToolRef] = field(default_factory=list)


@dataclass(frozen=True)
class Example:
    rank: int  # 2 = every term in the command, 1 = matched via intent/section
    label: str  # repo label
    file: str  # tool-notes/<x>.md (repo-relative)
    line: int  # 1-based line number
    section: str
    command: str
    intent: str


def _strip_fence(line: str) -> str:
    return re.sub(r"\s+", "", line[3:])


def parse_category(path: Path) -> Category:
    name = ""
    tools: list[ToolRef] = []
    for raw in path.read_text().splitlines():
        if not name and raw.startswith("# "):
            name = raw[2:].strip()
        m = _BULLET_RE.match(raw)
        if m:
            target = m.group("target")
            slug = Path(target).stem
            tools.append(
                ToolRef(slug=slug, display=m.group("display"), desc=(m.group("desc") or "").strip())
            )
    return Category(name=name or path.stem, slug=path.stem, file=path, tools=tools)


def list_categories(root: Root) -> list[Category]:
    cat_dir = root.categories_dir
    if not cat_dir.is_dir():
        return []
    return [parse_category(p) for p in sorted(cat_dir.glob("*.md"))]


def find_tool_category(root: Root, tool: str) -> tuple[Category, ToolRef] | None:
    """The category (and its bullet) currently referencing <tool>, if any."""
    for c in list_categories(root):
        for t in c.tools:
            if t.slug == tool:
                return c, t
    return None


def orphan_tools(root: Root, categories: list[Category]) -> list[str]:
    """Tool notes that exist but aren't referenced by any category file."""
    referenced = {t.slug for c in categories for t in c.tools}
    orphans = []
    for p in sorted(root.notes_dir.glob("*.md")):
        if p.name == "README.md":
            continue
        if p.stem not in referenced:
            orphans.append(p.stem)
    return orphans


def iter_examples(text: str):
    """Yield (line_no, section, command, intent) for indexable example lines."""
    title = ""
    section = ""
    in_block = False
    indexable = False
    for n, line in enumerate(text.splitlines(), start=1):
        if line.startswith("```"):
            if in_block:
                in_block = False
                indexable = False
            else:
                in_block = True
                indexable = _strip_fence(line) in _INDEXABLE_FENCES
            continue
        if not in_block:
            if not title and line.startswith("# "):
                title = line[2:]
            if re.match(r"^#{2,} ", line):
                section = re.sub(r"^#+\s+", "", line)
            continue
        if not indexable or not line.strip():
            continue
        m = _INTENT_RE.search(line)
        if m:
            intent = line[m.start() :].lstrip()
            command = line[: m.start()].strip()
        else:
            intent = ""
            command = line.strip()
        if not command:  # comment-only line: context, not a reusable command
            continue
        yield n, (section or title), command, intent


def find(roots: list[Root], terms: list[str]) -> list[Example]:
    words = [w.lower() for w in terms if w]
    results: list[Example] = []
    for root in roots:
        notes_dir = root.notes_dir
        if not notes_dir.is_dir():
            continue
        for path in sorted(notes_dir.glob("*.md")):
            if path.name == "README.md":
                continue
            for n, section, command, intent in iter_examples(path.read_text()):
                haystack = f"{command} {intent} {section}".lower()
                if not all(w in haystack for w in words):
                    continue
                cmd_l = command.lower()
                rank = 2 if all(w in cmd_l for w in words) else 1
                results.append(
                    Example(
                        rank=rank,
                        label=root.label,
                        file=f"tool-notes/{path.name}",
                        line=n,
                        section=section,
                        command=command,
                        intent=intent,
                    )
                )
    results.sort(key=lambda e: (-e.rank, e.label, e.file, e.line))
    return results
