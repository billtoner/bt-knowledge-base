# CLAUDE.md

Guide for Claude when working in this repo.

## What this repo is

A personal CLI cheat-sheet. The audience is the repo owner, refreshing on commands he has used before but doesn't use often. The job of each tool note is to **jog memory**, not teach from scratch — show real examples the way he last used them.

## Three-tier structure

1. **Top-level index** — `doc/bt-knowledge-base.md`. Lists categories only. Populated categories are links; empty categories are placeholders (plain text, no link).
2. **Category files** — `doc/categories/<kebab-case>.md`. One per category. Lists the tools in that category, each linking to its tool note. Short intro line is fine; no examples here.
3. **Tool notes** — `tool-notes/<tool>.md`. Where the actual examples live. One file per tool.

Examples never live in tiers 1 or 2 — only in tool notes.

## Path conventions

- `doc/bt-knowledge-base.md` → category file: `categories/<name>.md`
- `doc/categories/<x>.md` → tool note: `../../tool-notes/<name>.md`
- File names are kebab-case (`linux-services.md`, not `LinuxServices.md` or `linux_services.md`).

## Tool note style

Follow the shape of `tool-notes/ripgrep.md`:

```markdown
# tool-name (`short-cmd`)

One-line description: what it replaces or what it does.

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

## When the user provides input

- **He pastes examples** (from a file, a past terminal session, a message): treat his examples as the source of truth. Keep his exact commands; group by use case; add light annotations only if intent isn't obvious.
- **He describes a tool without examples**: propose useful real-world examples. Ask before writing more than ~15 example lines — he may want to provide his own.
- **He says "I use it for X"**: include an X section with his examples or, if none, a couple of proposed ones flagged as such.

## When adding a new tool

`kb add <tool>` (see `bin/kb`, documented in the README) automates all of the
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
