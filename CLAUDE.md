# CLAUDE.md

Guide for Claude when working in this repo.

## What this repo is

A personal knowledge base for the repo owner. It started as a CLI cheat-sheet and still holds many tool notes, but it's for **anything worth remembering** — home projects, recipes, how-tos, ideas. The job of every note is to **jog memory**, not teach from scratch. There are two note kinds:

- **Tool notes** — a CLI tool with real command examples (the original style; see below).
- **Prose notes** — plain text about anything, no commands (see "Prose note style").

Both live in the same store and are captured/searched/edited/deleted the same way via the `kb` CLI (`src/kb`, documented in the README). `kb find` searches command examples *and* prose body, so any note is findable.

## Three-tier structure

1. **Top-level index** — `doc/bt-knowledge-base.md`. Lists categories only. Populated categories are links; empty categories are placeholders (plain text, no link).
2. **Category files** — `doc/categories/<kebab-case>.md`. One per category. Lists the entries in that category, each linking to its note. Short intro line is fine; no examples here.
3. **Notes** — `tool-notes/<name>.md`. Where the content lives, one file per entry. (The directory name is historical — it holds every note kind, not just tools.)

Content never lives in tiers 1 or 2 — only in the notes. A note may also be **uncategorized** (no category-file bullet); it still lives in `tool-notes/`, is listed by `kb list` under "(uncategorized)", and is fully searchable. File it later with `kb move <name> <category>`.

## Path conventions

- `doc/bt-knowledge-base.md` → category file: `categories/<name>.md`
- `doc/categories/<x>.md` → tool note: `../../tool-notes/<name>.md`
- File names are kebab-case (`linux-services.md`, not `LinuxServices.md` or `linux_services.md`).

## Tool note style

Follow the shape of `tool-notes/ripgrep.md`:

```markdown
# tool-name (`short-cmd`)

One-line description: what it replaces or what it does.

**Tags:** tag-one · tag-two · tag-three

## Cool features

- **Bold headline.** Short sentence explaining the non-obvious capability.
- Aim for "I didn't remember it could do that" moments, not flag dumps.

## <Use-case heading>          (one section per real-world use case)

​```bash
cmd ...                # comment on intent, aligned for readability
cmd ...                # next example
​```

## Habit shifts from <old-tool>     (optional — only when replacing something)

| Old | New |
|---|---|
| `grep -rn x .` | `rg x` |

## Killer flags

- `-x` — what it does
- `-y` — what it does
```

Not every section is mandatory — only `# title` + 1-line description + at least one use-case block. Add `Cool features`, `Habit shifts`, and `Killer flags` when they earn their keep.

The optional `**Tags:**` line sits directly under the description (before the first `##`). Tags are cross-cutting, many-to-many labels — orthogonal to the single category — so `kb tag <tag>` can gather every entry for a job (e.g. `search`) across categories. Keep them lowercase kebab, separated by ` · ` (commas also parse). Reuse existing tags rather than coining near-duplicates; `kb tags` shows the current vocabulary. Categories still follow the one-home rule; tags don't replace them.

## Prose note style

For a non-tool entry (a home project, a recipe, an idea), skip the tool-note scaffolding entirely — no `Cool features`, no bash blocks. A prose note is just:

```markdown
# short-title

One-line summary of what this is.

**Tags:** tag-one · tag-two          (optional)

Write freely. Plain paragraphs and bullet lists. Add `## sections` only
once the note grows enough to need them.
```

`kb add <name> --prose` scaffolds exactly this (and `--category` is optional). Keep the title short and kebab-case — it's the filename slug *and* a search signal (`kb find` matches the title, so a word in the title makes the note findable even if the body doesn't repeat it). Everything else is freeform; the only rule is that the body is real content, not a template.

## When the user provides input

- **He pastes examples** (from a file, a past terminal session, a message): treat his examples as the source of truth. Keep his exact commands; group by use case; add light annotations only if intent isn't obvious.
- **He describes a tool without examples**: propose useful real-world examples. Ask before writing more than ~15 example lines — he may want to provide his own.
- **He says "I use it for X"**: include an X section with his examples or, if none, a couple of proposed ones flagged as such.

## When adding a new tool

`kb add <tool>` (see `src/kb`, documented in the README) automates all of the
below — scaffolding the note and wiring the category file, index link, and
README bullet. The manual steps, when not using it:

1. Write `tool-notes/<tool>.md` in the style above.
2. Add a bullet to the appropriate `doc/categories/<cat>.md`.
3. If the category file doesn't exist yet, create it, and convert its placeholder in `doc/bt-knowledge-base.md` to a link.

## When adding a new category

- Create `doc/categories/<kebab-case>.md` (one-line intro + tool list).
- Replace the placeholder in `doc/bt-knowledge-base.md` with a link to the new category file.

## Don'ts

- Don't put command examples in `doc/bt-knowledge-base.md` or in category files — examples belong in tool notes.
- Don't duplicate a tool across categories — pick one home.
- Don't create a category file with zero tools — leave it as a placeholder in the top-level index until there's something to put in it.
- Don't write tutorial prose. This is a cheat-sheet, not a manual.
- Don't add emojis or hype.
- Don't add "see also" cross-references unless they earn their keep.
