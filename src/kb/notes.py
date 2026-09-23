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
# A '## heading' (or deeper) section title.
_SECTION_RE = re.compile(r"^#{2,}\s+(.*)$")
# The cross-cutting tag line under a note's description:  **Tags:** search · files
_TAGS_RE = re.compile(r"^\*\*Tags:\*\*\s*(?P<tags>.+?)\s*$")
# How tags are written into a note (readable middot); parsing accepts commas too.
TAG_SEP = " · "


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
class TaggedTool:
    slug: str  # tool-note filename stem
    label: str  # repo label
    category: str  # its category name (empty if uncategorized)
    desc: str  # one-line description (from the category bullet)
    tags: tuple[str, ...]  # the tags on the note, in written order


@dataclass(frozen=True)
class Example:
    rank: int  # 2 = every term in the command, 1 = via intent/section, 0 = prose body
    label: str  # repo label
    file: str  # tool-notes/<x>.md (repo-relative)
    line: int  # 1-based line number
    section: str
    command: str  # the matched line: a shell command (kind="cmd") or prose (kind="prose")
    intent: str
    kind: str = "cmd"  # "cmd" = shell example line, "prose" = note body text


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


def list_sections(text: str) -> list[str]:
    """The '## heading' section titles in a note (ignoring headings inside fences)."""
    out: list[str] = []
    in_block = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_block = not in_block
            continue
        if not in_block:
            m = _SECTION_RE.match(line)
            if m:
                out.append(m.group(1).strip())
    return out


def note_tags(text: str) -> list[str]:
    """The tags on a note's '**Tags:**' line, lowercased and de-duped in order.

    The line lives just under the description, outside any code fence. Tags are
    split on the middot separator or commas, so both `a · b` and `a, b` parse.
    """
    in_block = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_block = not in_block
            continue
        if in_block:
            continue
        m = _TAGS_RE.match(line.strip())
        if m:
            out: list[str] = []
            for part in re.split(r"[·,]", m.group("tags")):
                t = part.strip().lower()
                if t and t not in out:
                    out.append(t)
            return out
    return []


def collect_tags(roots: list[Root]) -> list[TaggedTool]:
    """Every tagged tool note across all roots, with its category and description."""
    out: list[TaggedTool] = []
    for root in roots:
        notes_dir = root.notes_dir
        if not notes_dir.is_dir():
            continue
        info = {t.slug: (c.name, t.desc) for c in list_categories(root) for t in c.tools}
        for path in sorted(notes_dir.glob("*.md")):
            if path.name == "README.md":
                continue
            tags = note_tags(path.read_text())
            if not tags:
                continue
            cat, desc = info.get(path.stem, ("", ""))
            out.append(
                TaggedTool(
                    slug=path.stem, label=root.label, category=cat, desc=desc, tags=tuple(tags)
                )
            )
    return out


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


def iter_prose(text: str):
    """Yield (line_no, section, text) for note *body* lines — prose, bullets, table
    rows — excluding code fences, headings, the `**Tags:**` line, and blank lines.

    This is what makes non-shell notes (a recipe, a home-improvement thought)
    findable: iter_examples only sees inside ```code fences, iter_prose sees the rest.
    """
    title = ""
    section = ""
    in_block = False
    for n, line in enumerate(text.splitlines(), start=1):
        if line.startswith("```"):
            in_block = not in_block
            continue
        if in_block:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if re.match(r"^#{1,6} ", line):
            section = re.sub(r"^#+\s+", "", line).strip()
            continue
        if _TAGS_RE.match(stripped):
            continue
        # Strip a leading list marker for cleaner display; keep the text.
        display = re.sub(r"^\s*[-*+]\s+", "", line).strip()
        if display:
            yield n, (section or title), display


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
            text = path.read_text()
            rel = f"tool-notes/{path.name}"
            for n, section, command, intent in iter_examples(text):
                haystack = f"{command} {intent} {section}".lower()
                if not all(w in haystack for w in words):
                    continue
                cmd_l = command.lower()
                rank = 2 if all(w in cmd_l for w in words) else 1
                results.append(
                    Example(
                        rank=rank,
                        label=root.label,
                        file=rel,
                        line=n,
                        section=section,
                        command=command,
                        intent=intent,
                    )
                )
            for n, section, prose in iter_prose(text):
                haystack = f"{prose} {section}".lower()
                if not all(w in haystack for w in words):
                    continue
                results.append(
                    Example(
                        rank=0,
                        label=root.label,
                        file=rel,
                        line=n,
                        section=section,
                        command=prose,
                        intent="",
                        kind="prose",
                    )
                )
    results.sort(key=lambda e: (-e.rank, e.label, e.file, e.line))
    return results
