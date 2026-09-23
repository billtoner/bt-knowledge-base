# bt-knowledge-base

A personal knowledge base for anything worth remembering — CLI tools and their examples, but also home projects, recipes, ideas, how-tos. Each entry is its own page; a fast CLI captures, searches, edits, and deletes them.

## Start here

- **[doc/bt-knowledge-base.md](doc/bt-knowledge-base.md)** — the categorized index. Every entry lives under a category (or stays uncategorized until you file it).
- **[CLAUDE.md](CLAUDE.md)** — the three-tier structure (index → category files → notes), the two note kinds (tool notes and plain prose notes), and the style rules for adding entries.

## Find and capture with `kb`

`kb` is the day-to-day driver — get/put for your notes. It's a small
Python (Typer) CLI under `src/kb`; install it with pipx so it lands on your PATH:

```bash
pipx install --editable ~/repos/bt-knowledge-base   # provides the `kb` command

kb find <terms...>     # search EVERY note — shell examples AND prose body;
                       #   command matches rank first; prints snippet + file:line
kb list [category]     # categories and the entries under each (or just one);
                       #   -c category names only · -v also show each note's sections
kb cats [-v]           # category names only (-v adds counts)
kb tags [-v]           # the tag vocabulary — cross-cutting labels (-v adds counts)
kb tag <tag...>        # entries carrying a tag (several tags = entries with ALL of them);
                       #   e.g. `kb tag search` for every search-ish tool, then dig in
kb sections <name>     # the section headings inside a note
kb add <name> ...      # editor-first capture (scaffolds + wires a new note):
                       #   --category C      home for the note (OPTIONAL; else uncategorized)
                       #   --prose           plain prose note (no bash block) — for any thought
                       #   --tags "a,b"      tags (the **Tags:** line)
                       #   --section "H"      append under an existing section
                       #   --new-section "H"  create a section, then capture
kb open <name>         # open a note in $EDITOR — this is how you EDIT an entry
kb move <name> <cat>   # (re)categorize a note (updates category files + index)
kb delete <name>       # delete a note + unwire it (alias: rm; -y to skip confirm)
kb show <name>         # print a note (renders via glow/bat + pages via $PAGER
                       #   when interactive; raw+unpaged when piped or --raw;
                       #   --no-pager for inline; alias: cat)
kb --help              # common tasks + per-subcommand help
```

### Tags vs. categories

A tool has exactly one **category** — its home in the three-tier structure. **Tags** are
orthogonal and many-to-many: cross-cutting labels for "show me every tool I could reach for
when I'm doing X". `ripgrep` lives in *Search* but is tagged `search · text · files`; `fzf`,
`fd`, and `atuin` also carry `search`, so `kb tag search` gathers them all regardless of
category. Tags live on a `**Tags:**` line just under each note's description; `kb` derives the
whole vocabulary by scanning, so there's nothing to keep in sync. `kb tags` lists the
vocabulary (counts with `-v`); `kb tag <tag>` lists the tools, showing each one's other tags so
a query is a jumping-off point.

### Two repos, one tool

`kb` searches across multiple knowledge-base roots and writes to a chosen one.
Configure them in `~/.config/kb/roots` (or the `$KB_ROOTS` env var):

```
# label = path   (the FIRST root is the default write target)
pub  = ~/repos/bt-knowledge-base
priv = ~/repos/bt-knowledge-base-private
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
