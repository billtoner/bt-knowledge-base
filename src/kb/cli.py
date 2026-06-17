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
}


class AliasGroup(TyperGroup):
    def get_command(self, ctx, name):  # type: ignore[override]
        return super().get_command(ctx, _ALIASES.get(name, name))


app = typer.Typer(
    cls=AliasGroup,
    add_completion=False,
    no_args_is_help=True,
    help="get/put for your knowledge-base notes (a curated, searchable shell history).",
)

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


def _emit_categories(roots: list[Root]) -> None:
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
) -> None:
    """List categories and the tools under each; pass a category to show just that one."""
    roots = _roots()
    if categories:
        _emit_categories(roots)
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
def cats() -> None:
    """List category names only (the high-level buckets)."""
    _emit_categories(_roots())


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
def add(
    tool: str = typer.Argument(..., help="tool note to capture into"),
    section: str = typer.Option("", "--section", help="section to capture under"),
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
        insert_line = capture.find_insert_line(note.read_text(), section)
        if not insert_line:
            if section:
                _die(
                    f'no bash example block under section "{section}" in {rel(note)} '
                    "(check the heading, or omit --section)"
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


def main() -> None:
    try:
        app()
    except KbError as e:
        typer.echo(f"kb: {e}", err=True)
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
