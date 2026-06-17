"""kb — get/put for the bt-knowledge-base notes repo.

A curated, searchable "select shell history": commands worth keeping, each paired
with the reason you kept it (the inline `# intent` comment), living in
tool-notes/*.md under the three-tier structure (see CLAUDE.md).
"""

from __future__ import annotations

import os
import shlex
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

    - `kb find <terms>` — search every example (command, intent, or section)
    - `kb list [category]` — categories and the tools under each
    - `kb list -c` / `kb cats` — category names only
    - `kb list -v` — tools with each one's sections
    - `kb sections <tool>` — a tool's section headings
    - `kb add <tool> --category <C>` — new tool (category created if new)
    - `kb add <tool> --section "<H>"` — append under an existing section
    - `kb add <tool> --new-section "<H>"` — create a section, then capture
    - `kb move <tool> <category>` — recategorize a tool
    - `kb show <tool>` — print a note to the terminal (no editor)
    - `kb open <tool>` — open a note in $EDITOR
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
    """Search examples across all roots; prints command + intent + a file:line pointer."""
    roots = _roots()
    results = notes.find(roots, terms)
    if not results:
        typer.echo(f"kb: no examples match: {' '.join(terms)}")
        raise typer.Exit(1)
    show_label = len(roots) > 1
    for e in results:
        head = f"{CMD}{e.command}{RST}"
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
def show(tool: str = typer.Argument(..., help="tool note to print")) -> None:
    """Print a tool note to the terminal — like `open`, but no editor."""
    for root in _roots():
        note = root.notes_dir / f"{tool}.md"
        if note.is_file():
            typer.echo(note.read_text(), nl=False)
            return
    _die(f"no tool note: {tool} (try: kb find {tool})")


@app.command()
def add(
    tool: str = typer.Argument(..., help="tool note to capture into"),
    section: str = typer.Option("", "--section", help="existing section to capture under"),
    new_section: str = typer.Option("", "--new-section", help="create this section, then capture"),
    category: str = typer.Option("", "--category", help="category for a NEW tool"),
    desc: str = typer.Option("", "--desc", help="description for a NEW tool's title"),
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

    # New note: scaffold + wire category + README + index.
    if new_section:
        _die(f"{tool} doesn't exist yet — create it with --category first")
    if not category:
        category = typer.prompt(f"Category for new tool '{tool}' (e.g. Network)")
    if not category:
        _die("a category is required for a new tool")
    desc = desc or "<one-line description — what it does / what it replaces>"
    cat_slug = capture.kebab(category)
    cat_file = rt.categories_dir / f"{cat_slug}.md"

    if dry_run:
        typer.echo(f"DRY-RUN plan for new tool '{tool}':")
        typer.echo(f"  create  {rel(note)}")
        if cat_file.exists():
            typer.echo(f"  append bullet to {rel(cat_file)}")
        else:
            typer.echo(f"  create  {rel(cat_file)} (H1: {category}) + link it in {rel(rt.index)}")
        typer.echo(f"  append bullet to {rel(rt.readme)}")
        return

    capture.write_new_note(note, tool, desc)
    created = capture.add_category_bullet(cat_file, category, tool, desc)
    if created:
        capture.wire_index_category(rt.index, category, cat_slug)
        typer.echo(f"  linked category in {rel(rt.index)}")
    capture.add_readme_bullet(rt, tool, desc)
    typer.echo(f"Scaffolded new tool '{tool}' in category '{category}'.")
    typer.echo(f"  {rel(note)}")
    typer.echo(f"  {rel(cat_file)}")
    open_at(note, 8)


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


def main() -> None:
    try:
        app()
    except KbError as e:
        typer.echo(f"kb: {e}", err=True)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
