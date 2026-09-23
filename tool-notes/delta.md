# delta (git-delta)

Syntax-highlighted, side-by-side, language-aware git diff viewer. Works as a pager for
`git diff`, `git show`, `git log -p`, `git stash show -p`, etc.

**Tags:** git · diff · viewer

## Cool features

- **Side-by-side mode.** Left = old, right = new, instead of `-`/`+` stacked. Easier on big chunks.
- **Word-level highlighting.** Within a changed line, only the modified words light up bright;
  unchanged parts stay dimmed. Hugely useful for spotting one-char renames inside long lines.
- **Navigate between files.** `n` jumps to next file, `N` to previous, inside `git log -p` etc.
- **Syntax highlighting** based on file extension. Pick from many themes.
- **Hyperlinks (OSC 8).** With `hyperlinks = true`, file paths in diff output become clickable in
  supporting terminals (iTerm2). Cmd-click → opens in VS Code at the right line.
- **`git blame` beautification** when you set `[blame] coloring = highlightRecent`.
- **Direct file-diff** without git: `delta file1 file2`. Pipe patches: `delta < some.diff`.
- **`zdiff3` merge conflicts** show the common ancestor — much easier to resolve.

## Configuration (already in your `~/.gitconfig`)

```ini
[core]
    pager = delta
[interactive]
    diffFilter = delta --color-only
[delta]
    navigate = true
    side-by-side = true
    line-numbers = true
    syntax-theme = "Monokai Extended"
    # Optional:
    # hyperlinks = true
    # hyperlinks-file-link-format = "vscode://file/{path}:{line}"
[merge]
    conflictstyle = zdiff3
```

## Use it directly (outside the pager)

```bash
delta old.py new.py                       # diff two files without git
diff -u a.txt b.txt | delta               # pipe any unified diff through it
diff -ru dirA dirB | delta                # diff two directories
git diff | delta --side-by-side           # force side-by-side once
git -c delta.side-by-side=false diff      # force inline once (override config)
delta --width 120 old new                 # constrain width
delta --wrap-max-lines 3                  # wrap long lines instead of truncating
git blame -c app.js | bat -l git          # delta doesn't page blame — use bat instead
```

## Named feature sets (toggle groups of options)

```gitconfig
[delta]
    features = side-by-side line-numbers decorations
[delta "decorations"]
    commit-decoration-style = bold yellow box ul
    file-decoration-style   = none
[diff]
    colorMoved = default       # highlight moved-but-unchanged blocks
```

```bash
DELTA_FEATURES=+side-by-side git diff     # toggle a feature set per-invocation
```

## Useful in FPOC

```bash
git diff                                       # all current changes
git diff main..tools-upgrade                    # branch comparison
git show v0.8.20                                # a tagged commit
git log -p audiopulse/calibration/             # history with diffs, press `n` to skip files
git diff main...HEAD                            # what does THIS branch introduce vs main
git stash show -p                               # stash content
delta /tmp/before.txt /tmp/after.txt           # non-git file diff
```

## Theme audition

```bash
delta --show-syntax-themes                      # preview every theme on a sample
delta --list-syntax-themes                      # names only
DELTA_FEATURES="+syntax-theme:Dracula" git diff  # try one without committing to it
git config --global delta.syntax-theme "Nord"  # set permanently
```

## Killer interactive shortcut

`git log -p main..HEAD --reverse` + delta's `n`/`N` navigation = walk every commit of your branch
in sequence, hopping file-by-file. Feels like a GitHub diff view, in the terminal, faster.
