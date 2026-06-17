# bt-knowledge-base

A personal cheat-sheet of CLI tools and commands worth refreshing on. Each tool has its own page with real-world examples.

## Start here

- **[doc/bt-knowledge-base.md](doc/bt-knowledge-base.md)** — the categorized index. Every tool lives under a category.
- **[CLAUDE.md](CLAUDE.md)** — the three-tier structure (index → category files → tool notes) and the style rules for adding new entries.

## Find and capture with `kb`

`kb` is the day-to-day driver — a curated, searchable shell history. It's a small
Python (Typer) CLI under `src/kb`; install it with pipx so it lands on your PATH:

```bash
pipx install ~/Documents/repos/bt-knowledge-base   # provides the `kb` command

kb find <terms...>     # search every example by command, intent, or section;
                       # prints the snippet + a tool-notes/<x>.md:<line> pointer
kb list [category]     # categories and the tools under each (or just one);
                       #   -c category names only · -v also show each tool's sections
kb cats [-v]           # category names only (-v adds tool counts)
kb sections <tool>     # the section headings inside a tool note
kb add <tool> ...      # editor-first capture (scaffolds + wires a new tool/category):
                       #   --category C      home for a NEW tool
                       #   --section "H"      append under an existing section
                       #   --new-section "H"  create a section, then capture
kb move <tool> <cat>   # recategorize a tool (updates category files + index,
                       # removing a category that becomes empty)
kb open <tool>         # open a note in $EDITOR
kb --help              # common tasks + per-subcommand help
```

### Two repos, one tool

`kb` searches across multiple knowledge-base roots and writes to a chosen one.
Configure them in `~/.config/kb/roots` (or the `$KB_ROOTS` env var):

```
# label = path   (the FIRST root is the default write target)
pub  = ~/Documents/repos/bt-knowledge-base
priv = ~/Documents/repos/bt-knowledge-base-private
```

`kb find` searches **all** roots and tags each hit `[pub]` / `[priv]`. `kb add`
writes to the default (public) root; pass `--private` (or `--repo <label>`) to
target another, and it prints the destination so the target is never silent. The
two repos share only this tooling and the conventions in `CLAUDE.md` — content
stays separate. A root is skipped until it has a `tool-notes/` directory, so an
unset-up private repo is harmless.

## Browse with rendered links

```bash
grip . --browser              # serves the whole repo on localhost; relative links work
# then navigate to /doc/bt-knowledge-base.md
```

`grip .` is required (not `grip doc/bt-knowledge-base.md`) so that links from category files into `tool-notes/` — which live one directory above — can resolve. See [tool-notes/grip.md](tool-notes/grip.md) for more grip recipes.

## Setup on a fresh clone

Pre-commit hook configuration travels with the repo, but the git hook script
itself lives in `.git/hooks/` (untracked). After cloning:

```bash
brew install pre-commit         # if you don't have it yet
pre-commit install              # registers .git/hooks/pre-commit
```

This wires up the `gitleaks` secret-scanning hook defined in
[`.pre-commit-config.yaml`](.pre-commit-config.yaml). Tool notes and workflows
in this repo routinely describe credential formats (`glpat-…`, `AKIA…`,
`ghp_…`); the hook blocks commits that accidentally include a real one.
