# bat

`cat` with syntax highlighting, line numbers, and pager smarts.

**Tags:** viewer · files

## Cool features

- **Syntax highlighting** for ~200 languages — auto-detected from extension.
- **Line numbers** by default. Disable with `-p` or `--style=plain`.
- **Git status integration** — shows `+`/`-` next to lines that differ from HEAD.
- **Automatic paging** when output exceeds one screen; passes through when piped.
- **Themes.** `bat --list-themes` to preview; set with `--theme="Dracula"` or `BAT_THEME` env var.
- **Diff highlighting.** Pipe a diff in: `git diff | bat -l diff`.
- **Range printing.** `bat --line-range 50:100 file.py` (just lines 50-100).
- **Multiple files.** `bat file1 file2 file3` shows each with a header — easier than `cat` chains.

## Useful in FPOC

```bash
bat audiopulse/calibration/score.py              # pretty view of a module
bat -p audiopulse/__main__.py | head -30         # plain (no line nums) for piping-into-eyes
bat /tmp/commit-msg.txt                          # see proposed commit message in color
git diff | bat -l diff                            # if you don't have delta as pager
bat --diff README.md                              # show just the parts changed from git HEAD
```

## Viewing with focus (ranges + highlight)

```bash
bat -r 40:80 app.js                 # only lines 40-80 (great for big files)
bat -r 40:80 -H 55 app.js           # ...and highlight line 55
bat -H 12 -H 30 file.py             # highlight several lines
bat -A file                         # show non-printables (tabs, CR, trailing space)
bat --style=numbers,changes file    # just numbers + git changes, no grid/header
```

## Forcing a language (no extension / piped input)

```bash
curl -s https://api.example.com/x | bat -l json
kubectl get pod x -o yaml | bat -l yaml
git show HEAD | bat -l diff          # colorize ANY diff-shaped stream
some-cmd --help | bat -l help        # colorize help text
bat --list-languages | less          # what it can highlight
```

## Piping / scripting (turn OFF decorations)

```bash
bat -p file            # plain: no line numbers/grid/header (paste-friendly)
bat -pp file           # also disable paging
bat --color=always file | somecmd    # keep color through a pipe
```

## As an fzf preview (the classic pairing)

```bash
fzf --preview 'bat --color=always --style=numbers {}'
rg -n foo | fzf --delimiter : --preview 'bat --color=always -H {2} {1}'   # preview at file:line
```

## Themes & config

```bash
bat --list-themes                          # preview available themes
export BAT_THEME="Dracula"                 # or set in ~/.config/bat/config
```

`~/.config/bat/config`:
```
--theme="Dracula"
--style="numbers,changes,header"
--italic-text=always
```

## bat-extras (worth installing)

- `batgrep` — ripgrep results shown through bat
- `batman` — man pages via bat
- `batwatch` — like `watch`, highlighted
- `prettybat` — format + highlight
- `batdiff` — git-aware diff viewer

## Habit shifts from cat

`cat` still works fine for piping into other commands — `bat` auto-detects when it's not at a terminal and falls back to plain output. So you can just alias `cat=bat` if you want (most people don't, since `cat` is muscle memory).

## Useful side use: MANPAGER

```bash
# In ~/.zshrc
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
export MANROFFOPT="-c"          # fixes some man formatting with bat
```

Now `man rg`, `man bat`, etc., come out colored and scrollable.

## Killer flags

- `-p` / `--style=plain` — strip line numbers, headers, decorations
- `-r/-l start:end` — line range
- `--diff` — only changed lines vs HEAD
- `-l lang` — force a specific language highlighting
- `--theme="name"` — switch theme inline
