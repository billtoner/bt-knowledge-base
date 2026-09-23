# eza

Modern `ls` replacement. Maintained fork of the (defunct) `exa`.

**Tags:** files · listing

## Cool features

- **Git status column.** `eza --git` adds `--`, `-M`, `-N` etc. next to each file showing
  modified/new/ignored state. Replaces a separate `git status` for "what changed in this dir?"
- **Tree mode.** `eza --tree` recursively renders the directory as a tree. `--level 2` to limit depth.
- **Trailing markers (`ls -F`).** `eza -F` adds `/` after dirs, `*` after executables, `@` after
  symlinks. Identical to GNU `ls -F`.
- **Group directories first.** `--group-directories-first` (or `--group-directories-last`).
- **Icons** — `eza --icons` shows file-type emoji/Nerd Font glyphs. Requires a Nerd Font in your terminal.
- **Human-readable everywhere.** `-h` makes sizes "1.2K", "3.4M" etc. by default. (`-l` includes this.)
- **Header row.** `--header` adds column titles when listing.
- **Time field choice.** `--time=modified|accessed|created|changed` (the GNU `-t` flag is taken).

## Useful in FPOC

```bash
eza -lah --git audiopulse/                       # what changed in audiopulse/ since last commit
eza --tree --git-ignore audiopulse/calibration   # walk a module visually
eza -lah --git --sort=newest                     # newest-first listing
eza -lF                                           # quick ls with dir/exec markers
```

## Everyday power views

```bash
eza -la --git --group-directories-first        # long, all, git-status column, dirs first
eza -la --git --icons --time-style=relative     # "2 hours ago" + filetype icons
eza -lbGF --color-scale=size                    # shade sizes by magnitude
```

## Trees (with scoping)

```bash
eza --tree --level=3 -I '.git|node_modules|__pycache__'   # ignore noise
eza --tree --long --git --level=2 src                     # tree + git status per file
eza --tree --git-ignore                                   # respect .gitignore in the tree
```

## Sorting & sizes

```bash
eza -l --sort=size --reverse --total-size      # biggest first; real recursive dir sizes
eza -l --sort=extension                        # group by file type
eza -l --sort=created --time=created           # by creation time
eza -l --only-dirs --total-size                # dir sizes leaderboard
```

`--total-size` computes real recursive directory sizes (slower, but the honest number).

## Filtering

```bash
eza -l --git-ignore                            # hide gitignored files
eza -la -I '*.pyc|__pycache__'                 # glob ignore
eza -lD                                         # directories only
eza -lf                                         # files only (newer eza)
```

## Handy aliases (shell rc)

```bash
alias ls='eza --group-directories-first'
alias ll='eza -la --git --group-directories-first --icons'
alias lt='eza --tree --level=2 -I ".git|node_modules"'
alias lS='eza -l --sort=size --reverse --total-size'
```

## Clever combos

```bash
eza -la --git --sort=modified --reverse                    # what changed, newest first
eza -lD --total-size --sort=size --reverse                 # quick disk-hog scan of the top level
fd -t d | fzf --preview 'eza -la --git --color=always {}'  # peek a directory as an fzf preview
```

## Habit shifts from ls

| Old | New |
|---|---|
| `ls -la` | `eza -lah` |
| `ls -F` | `eza -F` (or `--classify`) |
| `ls -ltr` | `eza -l --sort=oldest` |
| `ls -lt` | `eza -l --sort=newest` |
| `tree` | `eza --tree` |

**Watch out**: `eza -t` is NOT "sort by time" (that conflicts with `--time=field`). Use `--sort=newest|oldest` instead. GNU muscle-memory pasting `-ltrp` will fail with "Option --time has no 'rp' setting" — that's the classic gotcha.

## Killer flags

- `--git` — git status column
- `--tree --level N` — tree view, depth-limited
- `-F` / `--classify` — type markers (`/` for dirs)
- `--icons` — file-type icons (needs Nerd Font)
- `--sort=newest|oldest|size|name` — explicit sort
- `--group-directories-first` — dirs at top
