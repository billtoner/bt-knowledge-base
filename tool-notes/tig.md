# tig

A TUI for browsing git history — log, diff, blame, refs, status, all keyboard-driven.

**Tags:** git · tui · viewer

## Cool features

- **Multiple view modes** (cycle with `m`, or launch directly):
    - `tig` — main log view
    - `tig blame FILE` — interactive blame, navigate from line to commit
    - `tig status` — git status as a TUI, stage hunks
    - `tig log` — pure log
    - `tig stash` — stash list
    - `tig grep "pattern"` — searchable grep results across history
    - `tig show <ref>` — single commit view
- **Quick navigation** — `j`/`k` next/prev, `Enter` to drill into diff, `q` to back out.
- **Blame drill-down.** In blame view, `Enter` on a line jumps to the commit that introduced it.
  Then `Enter` again to see the diff. You can chase a bug to its origin in seconds.
- **Three-pane mode** — main pane + a diff pane on the side. Live updates as you scroll commits.
- **Search.** `/` to search content; `?` for help in any view.
- **Refs view** (`r`) — branches and tags with selection.

## Useful in FPOC

```bash
tig                                              # browse history
tig audiopulse/webserver/WebServer.py            # history of one file
tig blame audiopulse/calibration/score.py        # who-when-why per line
tig status                                        # alternative to lazygit's status panel
tig main..tools-upgrade                           # commits introduced by branch
tig grep "compute_session_score"                  # search across history
```

## Tig vs lazygit (when to use which)

| Use case | Better tool |
|---|---|
| Stage hunks of a working-tree change | **lazygit** (or tig status) |
| Browse a sequence of commits | **tig** (fewer panels, more focused) |
| Trace "when did this line appear" via blame | **tig** (blame is its strength) |
| Interactive rebase | **lazygit** (visual squash/fixup) |
| Single-keystroke navigation through file history | **tig** |
| Multi-panel state at a glance | **lazygit** |

Both can live on your machine — they're for different headspaces.

## Keybindings cheat-sheet

| Key | Action |
|---|---|
| `j` / `k` | Next / prev line |
| `Enter` | Drill into commit / diff |
| `q` | Back / quit |
| `/` | Search forward |
| `n` / `N` | Next / prev search result |
| `m` | Switch view mode |
| `r` | Refs (branches/tags) |
| `t` | Tree view of HEAD |
| `?` | Help |
| `:` | Command prompt |

## Install

```bash
brew install tig
```

Not in your Brewfile yet — add it (or let the weekly refresh pick it up after you install).
