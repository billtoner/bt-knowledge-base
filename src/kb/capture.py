"""Write-side: scaffold new tool notes, wire them into the category/index/README
tiers, and insert ready-to-fill template lines into existing notes.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from .notes import _BULLET_RE, _INDEXABLE_FENCES, _SECTION_RE, TAG_SEP, _strip_fence
from .roots import Root

TEMPLATE = "command-here            # what it does / why you kept it"


def tag_line(tags: list[str]) -> str:
    """Render a '**Tags:**' line from raw tag strings (kebab-cased, de-duped)."""
    seen: list[str] = []
    for t in tags:
        k = kebab(t)
        if k and k not in seen:
            seen.append(k)
    return f"**Tags:** {TAG_SEP.join(seen)}" if seen else ""


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
# images: copy into the note's assets dir + insert a markdown link
# ---------------------------------------------------------------------------
def _same_bytes(a: Path, b: Path) -> bool:
    try:
        return a.read_bytes() == b.read_bytes()
    except OSError:
        return False


def _unique_path(p: Path) -> Path:
    """`p` if free, else `p-1`, `p-2`, … (suffix bumped before the extension)."""
    if not p.exists():
        return p
    i = 1
    while True:
        cand = p.with_name(f"{p.stem}-{i}{p.suffix}")
        if not cand.exists():
            return cand
        i += 1


def copy_image(root: Root, tool: str, src: Path) -> tuple[Path, str]:
    """Copy `src` into tool-notes/assets/<tool>/, returning (dest, note-relative link).

    An identical file already there is reused (no copy); a name clash with
    different content gets a `-1`/`-2` suffix so nothing is clobbered.
    """
    dest_dir = root.assets_dir / tool
    target = dest_dir / src.name
    if target.exists() and _same_bytes(target, src):
        return target, f"assets/{tool}/{target.name}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = _unique_path(target)
    shutil.copy2(src, target)
    return target, f"assets/{tool}/{target.name}"


# File extensions that render as an inline image (`![]()`); everything else is
# linked as a plain `[]()` so a PDF/doc opens or downloads instead of breaking.
IMAGE_EXTS = frozenset(
    {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif",
     ".heic", ".heif", ".ico", ".tif", ".tiff"}
)  # fmt: skip


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTS


def image_markdown(link: str, alt: str) -> str:
    return f"![{alt}]({link})"


def link_markdown(link: str, label: str) -> str:
    return f"[{label}]({link})"


def append_image(path: Path, markdown: str, section: str = "") -> int:
    """Insert an image line into a note — at the end of `section` if given (its
    caller validates the section exists), otherwise at the end of the file.
    Returns the 1-based line number of the inserted image line."""
    lines = path.read_text().splitlines()
    insert = len(lines)
    if section:
        want = section.strip().lower()
        in_block = found = False
        for i, line in enumerate(lines):
            if line.startswith("```"):
                in_block = not in_block
                continue
            if in_block:
                continue
            m = _SECTION_RE.match(line)
            if m and not found and m.group(1).strip().lower() == want:
                found = True
                continue
            if m and found:  # next heading ends the section
                insert = i
                break
    while insert > 0 and lines[insert - 1].strip() == "":  # trim trailing blanks
        insert -= 1
    lines[insert:insert] = ["", markdown]
    path.write_text("\n".join(lines).rstrip("\n") + "\n")
    return insert + 2  # the markdown line, after the inserted blank


def remove_assets(root: Root, tool: str) -> bool:
    """Delete a note's assets dir (tool-notes/assets/<tool>/). True if it existed."""
    d = root.assets_dir / tool
    if d.is_dir():
        shutil.rmtree(d)
        return True
    return False


def add_section(path: Path, heading: str, template: str = TEMPLATE) -> int:
    """Append a new '## heading' + bash block to a note. Returns the 1-based line
    of the inserted template line (for the editor to land on)."""
    text = path.read_text()
    if not text.endswith("\n"):
        text += "\n"
    text += f"\n## {heading}\n\n```bash\n{template}\n```\n"
    path.write_text(text)
    return len(text.splitlines()) - 1  # template sits just above the closing fence


# ---------------------------------------------------------------------------
# new notes: scaffold + wire category + index + README
# ---------------------------------------------------------------------------
PROSE_BODY = "<your note — write freely; add ## sections if it grows>"


def write_new_note(
    path: Path,
    tool: str,
    desc: str,
    template: str = TEMPLATE,
    tags: list[str] | None = None,
    prose: bool = False,
) -> int:
    """Scaffold a new note. Returns the 1-based line the editor should land on
    (the prose body for a prose note, the bash template line otherwise)."""
    lines = [f"# {tool}", "", desc, ""]
    tl = tag_line(tags or [])
    if tl:
        lines += [tl, ""]
    if prose:
        lines += [PROSE_BODY]
        land = len(lines)  # the body line
    else:
        lines += ["## Examples", "", "```bash", template, "```"]
        land = len(lines) - 1  # the template line, just above the closing fence
    path.write_text("\n".join(lines) + "\n")
    return land


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


def remove_readme_bullet(root: Root, tool: str) -> bool:
    """Remove the tool's bullet from tool-notes/README.md '## Tools'. Returns True
    if a bullet was removed."""
    readme = root.readme
    if not readme.exists():
        return False
    removed = False
    out: list[str] = []
    for line in readme.read_text().splitlines():
        m = re.match(r"^- \[[^\]]+\]\(([^)]+)\)", line)
        if m and Path(m.group(1)).stem == tool:
            removed = True
            continue
        out.append(line)
    if removed:
        readme.write_text("\n".join(out) + "\n")
    return removed


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
