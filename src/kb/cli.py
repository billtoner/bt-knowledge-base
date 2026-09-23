"""kb — get/put for the bt-knowledge-base notes repo.

A curated, searchable "select shell history": commands worth keeping, each paired
with the reason you kept it (the inline `# intent` comment), living in
tool-notes/*.md under the three-tier structure (see CLAUDE.md).
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

import typer
from typer.core import TyperGroup

from . import capture, notes
from .capture import KbError
from .roots import Root, load_roots, root_for

# --- command aliases (parity with the zsh dispatch) ---
_ALIASES = {
    "f": "find",
    "get": "find",
    "a": "add",
    "put": "add",
    "ls": "list",
    "l": "list",
    "c": "cats",
    "categories": "cats",
    "o": "open",
    "mv": "move",
    "sec": "sections",
    "cat": "show",
    "t": "tag",
    "tg": "tags",
    "rm": "delete",
    "del": "delete",
}


class AliasGroup(TyperGroup):
    def get_command(self, ctx, name):  # type: ignore[override]
        return super().get_command(ctx, _ALIASES.get(name, name))


app = typer.Typer(
    cls=AliasGroup,
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="markdown",
)


@app.callback()
def _root() -> None:
    """
    Curated, searchable shell history — get/put for your knowledge-base notes.

    **Common tasks**

    - `kb find <terms>` — search every note: shell examples AND prose body
    - `kb list [category]` — categories and the tools under each
    - `kb list -c` / `kb cats` — category names only
    - `kb list -v` — tools with each one's sections
    - `kb tags` — the tag vocabulary (cross-cutting; `-v` for counts)
    - `kb tag <tag...>` — tools carrying a tag (all tags = intersection)
    - `kb sections <tool>` — a tool's section headings
    - `kb add <tool> --category <C>` — new note (category optional)
    - `kb add <name> --prose` — new plain prose note (no bash block)
    - `kb add <tool> --section "<H>"` — append under an existing section
    - `kb add <tool> --new-section "<H>"` — create a section, then capture
    - `kb move <tool> <category>` — (re)categorize a note
    - `kb delete <name>` — delete a note and unwire it (alias: rm)
    - `kb show <tool>` — print a note to the terminal (no editor)
    - `kb open <tool>` — open a note in $EDITOR (this is how you *edit*)
    """


# --- colors (only when stdout is a tty) ---
_TTY = sys.stdout.isatty()
CMD = "\033[1m" if _TTY else ""
PATH = "\033[36m" if _TTY else ""
INT = "\033[2m" if _TTY else ""
SEC = "\033[33m" if _TTY else ""
RST = "\033[0m" if _TTY else ""


def _die(msg: str) -> NoReturn:
    typer.echo(f"kb: {msg}", err=True)
    raise typer.Exit(1)


def _fallback() -> Root | None:
    cwd = Path.cwd()
    return Root(cwd.name, cwd) if (cwd / "tool-notes").is_dir() else None


def _roots() -> list[Root]:
    roots = load_roots(_fallback())
    if not roots:
        _die("no knowledge-base roots configured; see ~/.config/kb/roots")
    return roots


def _tilde(p: Path) -> str:
    s, home = str(p), str(Path.home())
    return "~" + s[len(home) :] if s.startswith(home) else s


# Markdown renderers to try, in order of preference, when showing interactively.
_RENDERERS = (
    ["glow", "-"],  # true markdown rendering
    ["bat", "-l", "md", "--style=plain", "--paging=never"],  # colorized fallback
)


def render_markdown(text: str, raw: bool = False) -> None:
    """Print a note. Rendered through glow/bat when stdout is a TTY and one is
    available; raw otherwise — so pipes, redirects, and `--raw` stay verbatim."""
    if not raw and sys.stdout.isatty():
        for cmd in _RENDERERS:
            if shutil.which(cmd[0]):
                try:
                    subprocess.run(cmd, input=text, text=True, check=True)
                    return
                except (subprocess.SubprocessError, OSError):
                    continue
    typer.echo(text, nl=False)


def open_at(path: Path, line: int) -> None:
    ed = os.environ.get("EDITOR", "vi")
    parts = shlex.split(ed) or [ed]
    base = os.path.basename(parts[0])
    if "code" in ed:
        cmd = [*parts, "-g", f"{path}:{line}"]
    elif "vi" in base or "nvim" in base:
        cmd = [*parts, f"+{line}", str(path)]
    else:
        cmd = [*parts, str(path)]
    subprocess.run(cmd)


def _emit_categories(roots: list[Root], verbose: bool = False) -> None:
    """Print category names only (shared by `cats` and `list --categories`)."""
    multi = len(roots) > 1
    for root in roots:
        cats_ = notes.list_categories(root)
        if multi:
            typer.echo(f"{PATH}[{root.label}]{RST}")
        if not cats_:
            typer.echo(f"  {INT}(no categories yet){RST}")
            continue
        for c in cats_:
            if verbose:
                typer.echo(f"{c.name}  {INT}({len(c.tools)}){RST}")
            else:
                typer.echo(c.name)


# ---------------------------------------------------------------------------
@app.command()
def find(terms: list[str] = typer.Argument(..., help="search terms")) -> None:
    """Search every note across all roots — shell examples and prose body alike.

    All terms must match (in the command, its intent, the section, or the prose).
    Command matches rank above prose; prints the line + a file:line pointer.
    """
    roots = _roots()
    results = notes.find(roots, terms)
    if not results:
        typer.echo(f"kb: no examples match: {' '.join(terms)}")
        raise typer.Exit(1)
    show_label = len(roots) > 1
    for e in results:
        # Shell examples print bold; prose body prints plain so it reads naturally.
        head = f"{CMD}{e.command}{RST}" if e.kind == "cmd" else e.command
        if e.intent:
            head += f"   {INT}{e.intent}{RST}"
        typer.echo(head)
        loc = "  "
        if show_label:
            loc += f"{INT}[{e.label}]{RST} "
        loc += f"{PATH}{e.file}:{e.line}{RST}"
        if e.section:
            loc += f"  {INT}·  {RST}{SEC}{e.section}{RST}"
        typer.echo(loc)
        typer.echo("")
    typer.echo(f"{INT}{len(results)} match(es).{RST}")


@app.command("list")
def list_cmd(
    category: str | None = typer.Argument(None, help="show only this category"),
    categories: bool = typer.Option(
        False, "--categories", "-c", help="show only category names (no tools)"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="show each tool's sections (or counts with -c)"
    ),
) -> None:
    """List categories and the tools under each; pass a category to show just that one."""
    roots = _roots()
    if categories:
        _emit_categories(roots, verbose)
        return
    multi = len(roots) > 1
    filt = capture.kebab(category) if category else ""
    matched = False
    for root in roots:
        cats = notes.list_categories(root)
        if filt:
            cats = [c for c in cats if c.slug == filt]
            if not cats:
                continue
        if multi:
            typer.echo(f"{PATH}[{root.label}]{RST}")
        for c in cats:
            matched = True
            typer.echo(f"{CMD}{c.name}{RST}")
            for t in c.tools:
                if t.desc:
                    typer.echo(f"  {t.slug}  {INT}{t.desc}{RST}")
                else:
                    typer.echo(f"  {t.slug}")
                if verbose:
                    note = root.notes_dir / f"{t.slug}.md"
                    if note.is_file():
                        for s in notes.list_sections(note.read_text()):
                            typer.echo(f"      {INT}{s}{RST}")
        if filt:
            continue
        orphans = notes.orphan_tools(root, cats)
        if orphans:
            typer.echo(f"{SEC}(uncategorized){RST}")
            for o in orphans:
                typer.echo(f"  {o}")
        if not cats and not orphans:
            typer.echo(f"  {INT}(no tools yet){RST}")
    if filt and not matched:
        _die(f'no category matching "{category}" (try: kb cats)')


@app.command()
def cats(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="show tool counts"),
) -> None:
    """List category names only (the high-level buckets)."""
    _emit_categories(_roots(), verbose)


@app.command()
def tags(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="show tool counts per tag"),
) -> None:
    """List the tag vocabulary — the cross-cutting labels you can query with `kb tag`."""
    roots = _roots()
    counts: dict[str, int] = {}
    for tt in notes.collect_tags(roots):
        for t in tt.tags:
            counts[t] = counts.get(t, 0) + 1
    if not counts:
        typer.echo(f"{INT}(no tags yet — add a **Tags:** line to a note, or `kb add --tags`){RST}")
        return
    for name in sorted(counts):
        if verbose:
            typer.echo(f"{name}  {INT}({counts[name]}){RST}")
        else:
            typer.echo(name)


@app.command()
def tag(
    tags_: list[str] = typer.Argument(..., help="tag(s); multiple = tools with ALL of them"),
) -> None:
    """List tools carrying a tag (pass several tags to intersect them)."""
    roots = _roots()
    want = {capture.kebab(t) for t in tags_}
    hits = [tt for tt in notes.collect_tags(roots) if want <= set(tt.tags)]
    if not hits:
        _die(f"no tools tagged {' + '.join(sorted(want))} (try: kb tags)")
    show_label = len(roots) > 1
    hits.sort(key=lambda tt: (tt.category, tt.slug))
    for tt in hits:
        line = f"  {CMD}{tt.slug}{RST}"
        if tt.desc:
            line += f"  {INT}{tt.desc}{RST}"
        typer.echo(line)
        loc = "    "
        if show_label:
            loc += f"{INT}[{tt.label}]{RST} "
        loc += f"{SEC}{tt.category or '(uncategorized)'}{RST}"
        # surface the tool's OTHER tags, so a query is a jumping-off point
        others = [t for t in tt.tags if t not in want]
        if others:
            loc += f"  {INT}·  {' '.join(others)}{RST}"
        typer.echo(loc)
    typer.echo(f"{INT}{len(hits)} tool(s) tagged {' + '.join(sorted(want))}.{RST}")


@app.command()
def sections(tool: str = typer.Argument(..., help="tool note whose sections to list")) -> None:
    """List the section headings in a tool note (searches all roots)."""
    for root in _roots():
        note = root.notes_dir / f"{tool}.md"
        if note.is_file():
            secs = notes.list_sections(note.read_text())
            if not secs:
                typer.echo(f"{INT}(no sections){RST}")
                return
            for s in secs:
                typer.echo(s)
            return
    _die(f"no tool note: {tool} (try: kb find {tool})")


@app.command("open")
def open_cmd(tool: str = typer.Argument(..., help="tool note to open")) -> None:
    """Open a tool note in $EDITOR (searches all roots)."""
    for root in _roots():
        note = root.notes_dir / f"{tool}.md"
        if note.is_file():
            open_at(note, 1)
            return
    _die(f"no tool note: {tool} (try: kb find {tool})")


@app.command()
def show(
    tool: str = typer.Argument(..., help="note to print"),
    raw: bool = typer.Option(False, "--raw", "-r", help="print raw markdown (no rendering)"),
) -> None:
    """Print a note to the terminal — like `open`, but no editor.

    Renders the markdown (via glow/bat) when viewed interactively; prints raw
    when piped, redirected, or with --raw, so `kb show x | glow -` still works.
    """
    for root in _roots():
        note = root.notes_dir / f"{tool}.md"
        if note.is_file():
            render_markdown(note.read_text(), raw=raw)
            return
    _die(f"no note: {tool} (try: kb find {tool})")


@app.command()
def add(
    tool: str = typer.Argument(..., help="tool note to capture into"),
    section: str = typer.Option("", "--section", help="existing section to capture under"),
    new_section: str = typer.Option("", "--new-section", help="create this section, then capture"),
    category: str = typer.Option("", "--category", help="category for a NEW note (optional)"),
    desc: str = typer.Option("", "--desc", help="description for a NEW note's title"),
    tags: str = typer.Option("", "--tags", help="comma-separated tags for a NEW note"),
    prose: bool = typer.Option(False, "--prose", help="scaffold a plain prose note (no bash)"),
    private: bool = typer.Option(False, "--private", help="write to the private root"),
    repo: str = typer.Option("", "--repo", help="write to the root with this label"),
    dry_run: bool = typer.Option(False, "--dry-run", help="print planned changes"),
) -> None:
    """Editor-first capture; scaffolds + wires a new tool/category."""
    roots = _roots()
    sel = "private" if private else repo
    rt = root_for(roots, sel)
    if rt is None:
        labels = ", ".join(r.label for r in roots)
        _die(f"no {sel or 'default'} repo configured (roots: {labels}); see ~/.config/kb/roots")
    assert rt is not None
    typer.echo(f"{SEC}→ {rt.label} repo:{RST} {_tilde(rt.path)}")

    note = rt.notes_dir / f"{tool}.md"

    def rel(p) -> str:
        return str(Path(p).relative_to(rt.path))

    if note.is_file():
        if tags:
            _die(f"{tool} already exists — edit its **Tags:** line directly (kb open {tool})")
        if section and new_section:
            _die("pass either --section or --new-section, not both")
        if new_section:
            if new_section in notes.list_sections(note.read_text()):
                _die(f"section '{new_section}' already exists in {rel(note)} — use --section")
            if dry_run:
                typer.echo(f"DRY-RUN: would add section '{new_section}' to {rel(note)}")
                return
            line = capture.add_section(note, new_section)
            typer.echo(f"Added section '{new_section}' to {rel(note)}:{line} — fill it in.")
            open_at(note, line)
            return
        insert_line = capture.find_insert_line(note.read_text(), section)
        if not insert_line:
            if section:
                _die(
                    f'no bash example block under section "{section}" in {rel(note)} '
                    "(check the heading, or use --new-section to create it)"
                )
            _die(f"no bash example block in {rel(note)}; add one first or pass --section")
        if dry_run:
            typer.echo(f"DRY-RUN: would insert into {rel(note)} before line {insert_line}:")
            typer.echo(f"    {capture.TEMPLATE}")
            typer.echo(f"DRY-RUN: would open editor at line {insert_line}")
            return
        capture.insert_template(note, insert_line)
        typer.echo(f"Added template to {rel(note)}:{insert_line} — fill it in.")
        open_at(note, insert_line)
        return

    # New note: scaffold, then wire README + (optionally) category + index.
    if new_section:
        _die(f"{tool} doesn't exist yet — create it with --category first")
    desc = desc or "<one-line description — what it does / what it replaces>"
    cat_slug = capture.kebab(category) if category else ""
    cat_file = rt.categories_dir / f"{cat_slug}.md" if category else None

    if dry_run:
        typer.echo(f"DRY-RUN plan for new note '{tool}':")
        typer.echo(f"  create  {rel(note)}" + ("  (prose)" if prose else ""))
        if cat_file is None:
            typer.echo("  leave uncategorized (file later with: kb move)")
        elif cat_file.exists():
            typer.echo(f"  append bullet to {rel(cat_file)}")
        else:
            typer.echo(f"  create  {rel(cat_file)} (H1: {category}) + link it in {rel(rt.index)}")
        typer.echo(f"  append bullet to {rel(rt.readme)}")
        return

    tag_list = [t for t in tags.replace(",", " ").split() if t]
    land = capture.write_new_note(note, tool, desc, tags=tag_list, prose=prose)
    capture.add_readme_bullet(rt, tool, desc)
    if cat_file is not None:
        created = capture.add_category_bullet(cat_file, category, tool, desc)
        if created:
            capture.wire_index_category(rt.index, category, cat_slug)
            typer.echo(f"  linked category in {rel(rt.index)}")
        typer.echo(f"Scaffolded new note '{tool}' in category '{category}'.")
        typer.echo(f"  {rel(cat_file)}")
    else:
        typer.echo(
            f"Scaffolded '{tool}' (uncategorized — file it later with: kb move {tool} <cat>)."
        )
    typer.echo(f"  {rel(note)}")
    open_at(note, land)


@app.command()
def move(
    tool: str = typer.Argument(..., help="tool note to move"),
    category: str = typer.Argument(..., help="destination category"),
    private: bool = typer.Option(False, "--private", help="operate on the private root"),
    repo: str = typer.Option("", "--repo", help="operate on the root with this label"),
    dry_run: bool = typer.Option(False, "--dry-run", help="print planned changes"),
) -> None:
    """Move a tool from its current category to another (wiring/unwiring the index)."""
    roots = _roots()
    sel = "private" if private else repo
    rt = root_for(roots, sel)
    if rt is None:
        labels = ", ".join(r.label for r in roots)
        _die(f"no {sel or 'default'} repo configured (roots: {labels})")

    hit = notes.find_tool_category(rt, tool)
    if hit is None:
        _die(f"{tool} isn't in any category in the {rt.label} repo (try: kb find {tool})")
    old_cat, ref = hit
    target_slug = capture.kebab(category)

    def rel(p) -> str:
        return str(Path(p).relative_to(rt.path))

    if old_cat.slug == target_slug:
        typer.echo(f"{tool} is already in {old_cat.name}.")
        return

    new_cat_file = rt.categories_dir / f"{target_slug}.md"
    empties = all(t.slug == tool for t in old_cat.tools)

    if dry_run:
        typer.echo(f"DRY-RUN: move {tool}: {old_cat.name} → {category}")
        if new_cat_file.exists():
            typer.echo(f"  append bullet to {rel(new_cat_file)}")
        else:
            typer.echo(f"  create {rel(new_cat_file)} + link it in {rel(rt.index)}")
        typer.echo(f"  remove bullet from {rel(old_cat.file)}")
        if empties:
            typer.echo(f"  {old_cat.name} becomes empty → delete it and unlink from index")
        return

    created = capture.add_category_bullet(
        new_cat_file, category, tool, ref.desc, display=ref.display
    )
    if created:
        capture.wire_index_category(rt.index, category, target_slug)
    if capture.remove_category_bullet(old_cat.file, tool):
        old_cat.file.unlink()
        capture.unwire_index_category(rt.index, old_cat.slug)
        typer.echo(f"Moved {tool}: {old_cat.name} → {category} (removed empty {old_cat.name}).")
    else:
        typer.echo(f"Moved {tool}: {old_cat.name} → {category}.")


@app.command()
def delete(
    tool: str = typer.Argument(..., help="note to delete"),
    force: bool = typer.Option(False, "--force", "-y", help="skip the confirmation prompt"),
    private: bool = typer.Option(False, "--private", help="operate on the private root"),
    repo: str = typer.Option("", "--repo", help="operate on the root with this label"),
    dry_run: bool = typer.Option(False, "--dry-run", help="print planned changes"),
) -> None:
    """Delete a note and unwire it from its category, the index, and the README."""
    roots = _roots()
    sel = "private" if private else repo
    rt = root_for(roots, sel)
    if rt is None:
        labels = ", ".join(r.label for r in roots)
        _die(f"no {sel or 'default'} repo configured (roots: {labels})")

    note = rt.notes_dir / f"{tool}.md"
    if not note.is_file():
        _die(f"no note '{tool}' in the {rt.label} repo (try: kb find {tool})")

    def rel(p) -> str:
        return str(Path(p).relative_to(rt.path))

    hit = notes.find_tool_category(rt, tool)
    old_cat = hit[0] if hit else None
    empties = old_cat is not None and all(t.slug == tool for t in old_cat.tools)

    if dry_run:
        typer.echo(f"DRY-RUN: delete {tool} from the {rt.label} repo:")
        typer.echo(f"  remove {rel(note)}")
        if old_cat is not None:
            typer.echo(f"  remove bullet from {rel(old_cat.file)}")
            if empties:
                typer.echo(f"  {old_cat.name} becomes empty → delete it and unlink from index")
        else:
            typer.echo("  (uncategorized — nothing to unwire)")
        typer.echo(f"  remove bullet from {rel(rt.readme)}")
        return

    if not force and not typer.confirm(f"Delete note '{tool}' from the {rt.label} repo?"):
        typer.echo("Aborted.")
        raise typer.Exit(1)

    note.unlink()
    capture.remove_readme_bullet(rt, tool)
    if old_cat is not None:
        if capture.remove_category_bullet(old_cat.file, tool):
            old_cat.file.unlink()
            capture.unwire_index_category(rt.index, old_cat.slug)
            typer.echo(f"Deleted {tool} (removed empty {old_cat.name}).")
        else:
            typer.echo(f"Deleted {tool} from {old_cat.name}.")
    else:
        typer.echo(f"Deleted {tool} (was uncategorized).")


def main() -> None:
    try:
        app()
    except KbError as e:
        typer.echo(f"kb: {e}", err=True)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
