# lazygit

Full-screen TUI for git. Replaces command-flag memorization with keybindings + visual diffs.

**Tags:** git · tui

## Launch + orientation

```bash
lazygit                  # from any git repo
```

Five panels you'll use:
1. **Status** (top-left) — current branch, head info
2. **Files** (left, mid) — modified/untracked files; this is where you stage
3. **Branches** (left, lower) — list of branches; checkout, create, merge
4. **Commits** (mid) — git log; reword, squash, drop
5. **Stash** (bottom-left) — stashed changes

The big panel on the right shows live context (file diff, commit details, etc.).

## Cool features (by task)

### Stage hunks (the killer feature)

1. Highlight file in Files panel
2. `Enter` to drill into hunk-by-hunk mode
3. `space` to stage current hunk
4. `v`, arrow keys, `space` to stage individual lines

Replaces the entire `git add -p` interactive dance. Letting you cleanly separate one big change
into multiple focused commits.

### Commit

1. Stage files (`space` in Files panel)
2. `c` to commit, type message, Enter

### Amend last commit

1. Stage additional files (`space`)
2. `A` (capital) — amends the last commit

### Interactive rebase

1. **Commits** panel → highlight parent commit
2. `e` starts rebase from its child
3. Per-commit: `s` (squash into previous), `f` (fixup), `d` (drop), `r` (reword)
4. `M` (capital) to continue

### Browse file history

1. Files panel → highlight file → `enter` to drill in
2. `shift-K` shows commits touching just that file
3. `enter` on commit to see diff

### Conflict resolution

1. Conflicted files show with a yellow flag
2. `enter` on the file
3. `space` per hunk to pick version (ours/theirs/both)

### Stash to switch branches with uncommitted work

1. Files: `s` (stash all) or `shift-S` (stash with message)
2. Branches: `space` on target branch to checkout
3. After work, back to original branch
4. Stash panel: `g` to pop

## Useful in FPOC

- Reviewing what changed before committing — the diff appears automatically, no `git diff` needed
- Cleaning up a series of WIP commits with `e` rebase
- Browsing FPOC history with `shift-K` on a file like `WebServer.py`
- Stash workflow when you need to hop branches mid-task

## Universal shortcuts

| Key | Action |
|---|---|
| `?` | Help (in any panel) |
| `x` | Menu (more commands) |
| `R` | Refresh |
| `q` | Quit |
| `/` | Search/filter in panel |
| `tab` | Cycle panels |
| `1`–`5` | Jump to specific panel |
| `[` / `]` | Previous/next tab within a panel |
| `P` (capital) | Push |
| `p` (lower) | Pull |

## When NOT to use lazygit

- One-line git ops you've already memorized (`git add foo && git commit -m "..."` is faster than launching a TUI)
- Scripts/automation — lazygit is interactive only
- Anything you'd do inside a piped command sequence

For everything else (especially review-before-commit and history navigation), lazygit beats memorizing flags.
