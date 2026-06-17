"""Write-side: scaffold new tool notes, wire them into the category/index/README
tiers, and insert ready-to-fill template lines into existing notes.
"""

from __future__ import annotations

import re
from pathlib import Path

from .notes import _BULLET_RE, _INDEXABLE_FENCES, _strip_fence
from .roots import Root

TEMPLATE = "command-here            # what it does / why you kept it"


class KbError(Exception):
    """User-facing error; cli turns it into a styled message + exit 1."""


def _bullet(display: str, slug: str, desc: str) -> str:
    base = f"- [{display}](../../tool-notes/{slug}.md)"
    return f"{base} — {desc}" if desc else base


def kebab(s: str) -> str:
    """'AWS CLI' -> 'aws-cli', 'File and Directory' -> 'file-and-directory'."""
    s = re.sub(r"[^a-z0-9]+", "-", s.lower())
    return s.strip("-")


# ---------------------------------------------------------------------------
# existing notes: insert a template line at the end of a bash block
# ---------------------------------------------------------------------------
def find_insert_line(text: str, section: str = "") -> int:
    """Line number of the target bash block's CLOSING fence (0 if none).

    With a section, target the block under the matching '## heading'; otherwise
    the last indexable block in the file. Insert the template *before* this line.
    """
    want = (section or "").lower()
    in_block = indexable = False
    sec = ""
    last = target = 0
    for n, line in enumerate(text.splitlines(), start=1):
        if line.startswith("```"):
            if in_block:
                in_block = False
                if indexable:
                    last = n
                    if want and sec.lower() == want:
                        target = n
                indexable = False
            else:
                in_block = True
                indexable = _strip_fence(line) in _INDEXABLE_FENCES
            continue
        if not in_block and re.match(r"^#{2,} ", line):
            sec = re.sub(r"^#+\s+", "", line)
    return target if section else last


def insert_template(path: Path, insert_line: int, template: str = TEMPLATE) -> None:
    lines = path.read_text().splitlines(keepends=True)
    lines.insert(insert_line - 1, template + "\n")
    path.write_text("".join(lines))


# ---------------------------------------------------------------------------
# new notes: scaffold + wire category + index + README
# ---------------------------------------------------------------------------
def write_new_note(path: Path, tool: str, desc: str, template: str = TEMPLATE) -> None:
    path.write_text(f"# {tool}\n\n{desc}\n\n## Examples\n\n```bash\n{template}\n```\n")


def add_category_bullet(
    cat_file: Path, category: str, tool: str, desc: str, display: str | None = None
) -> bool:
    """Append the tool bullet to its category file. Returns True if the category
    file was newly created (so the caller knows to wire the index)."""
    bullet = _bullet(display or tool, tool, desc)
    if cat_file.exists():
        text = cat_file.read_text()
        if not text.endswith("\n"):
            text += "\n"
        cat_file.write_text(text + bullet + "\n")
        return False
    cat_file.write_text(f"# {category}\n\n{category} tools.\n\n{bullet}\n")
    return True


def remove_category_bullet(cat_file: Path, tool: str) -> bool:
    """Remove the bullet referencing <tool> from a category file. Returns True if
    no tool bullets remain afterward (the category is now empty)."""
    out: list[str] = []
    for line in cat_file.read_text().splitlines():
        m = _BULLET_RE.match(line)
        if m and Path(m.group("target")).stem == tool:
            continue
        out.append(line)
    cat_file.write_text("\n".join(out).rstrip("\n") + "\n")
    return not any(_BULLET_RE.match(line) for line in out)


def unwire_index_category(index: Path, slug: str) -> None:
    """Remove a category's link line from the index (used when it's emptied)."""
    needle = f"(categories/{slug}.md)"
    out = [line for line in index.read_text().splitlines() if needle not in line]
    index.write_text("\n".join(out) + "\n")


def wire_index_category(index: Path, name: str, slug: str) -> None:
    """Convert the category's placeholder to a link, or insert a new link in
    alpha order within the '## Categories' section."""
    link = f"- [{name}](categories/{slug}.md)"
    out: list[str] = []
    done = False
    incat = False
    for line in index.read_text().splitlines():
        if line.startswith("## "):
            if line.startswith("## Categories"):
                incat = True
                out.append(line)
                continue
            if incat and not done:
                out.append(link)
                done = True
            incat = False
        if incat and not done:
            if line.startswith("_No categories"):
                out.append(link)
                done = True
                continue
            if line.startswith("- "):
                item = line[2:]
                label = re.sub(r"\].*$", "", re.sub(r"^\[", "", item))
                if item == name:  # replace a plain placeholder
                    out.append(link)
                    done = True
                    continue
                cmp = label if item.startswith("[") else item
                if cmp.lower() > name.lower():
                    out.append(link)
                    done = True
        out.append(line)
    if not done:
        out.append(link)
    index.write_text("\n".join(out) + "\n")


def add_readme_bullet(root: Root, tool: str, desc: str) -> None:
    """Insert an alphabetical bullet into tool-notes/README.md '## Tools'
    (bootstrapping the file if missing)."""
    bullet = f"- [{tool}]({tool}.md) — {desc}"
    readme = root.readme
    if not readme.exists():
        readme.write_text(
            "# tool-notes\n\nThe notes themselves. One file per tool, with "
            f"real-world examples.\n\n## Tools\n\n{bullet}\n"
        )
        return
    out: list[str] = []
    inlist = False
    done = False
    for line in readme.read_text().splitlines():
        if line.startswith("## "):
            if line.startswith("## Tools"):
                inlist = True
                out.append(line)
                continue
            if inlist and not done:
                out.append(bullet)
                done = True
            inlist = False
        if inlist and not done:
            if line.startswith("_No tool"):
                out.append(bullet)
                done = True
                continue
            if line.startswith("- ["):
                item = re.sub(r"\].*$", "", line[3:])
                if item.lower() > tool.lower():
                    out.append(bullet)
                    done = True
        out.append(line)
    if not done:
        out.append(bullet)
    readme.write_text("\n".join(out) + "\n")
