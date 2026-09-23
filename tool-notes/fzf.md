# fzf

General-purpose fuzzy filter: pipe a list in, get the selection(s) out. Its power is `--preview`, the `--bind` actions (`reload`, `become`), and `-m` (multi-select) into `xargs`.

**Tags:** search · fuzzy · interactive · shell

## Cool features

- **`become(cmd {})`** — replace fzf with a command (cleaner than command substitution for editors). fzf >= 0.38.
- **`reload(cmd {q})`** — re-run a command as you type (`{q}` = current query); the basis of live-grep.
- **`--preview`** turns any picker into a browser; `--delimiter` + `{1}`/`{2}` split each line into fields.
- **`-m`** multi-select (Tab to mark, Shift-Tab to unmark) feeds bulk actions through `xargs`.
- **`--preview-window 'up,60%,+{2}/2'`** centers a match line inside the preview.

## The crown jewel: interactive ripgrep → open at the exact line

Type to search file *contents* live; Enter opens `$EDITOR` on the matching line.

```bash
rg --line-number --no-heading --color=always '' \
  | fzf --ansi --delimiter : \
        --preview 'bat --color=always --highlight-line {2} {1}' \
        --preview-window 'up,60%,+{2}/2' \
        --bind 'enter:become($EDITOR {1} +{2})'      # {1}=file, {2}=line
```

### Two-mode version: fuzzy-filter vs. re-run ripgrep

Start in ripgrep mode (each keystroke re-runs `rg`), toggle to plain fuzzy filtering:

```bash
INITIAL="foo"
: | fzf --ansi --disabled --query "$INITIAL" \
      --bind "start:reload:rg --line-number --no-heading --color=always {q}" \
      --bind "change:reload:rg --line-number --no-heading --color=always {q} || true" \
      --bind 'ctrl-f:unbind(change)+change-prompt(fuzzy> )+enable-search' \
      --delimiter : \
      --preview 'bat --color=always --highlight-line {2} {1}' \
      --bind 'enter:become($EDITOR {1} +{2})'
```

## Previews turn fzf into a browser

```bash
fzf --preview 'bat --color=always {}'                       # file picker + syntax preview
fzf --preview 'bat --color=always {}' --bind 'ctrl-/:toggle-preview'
fd -t d | fzf --preview 'ls -la {}'                         # dir picker
```

## Git, made interactive

```bash
git log --oneline --color=always | fzf --ansi \
  --preview 'git show --color=always {1}' --bind 'enter:become(git show {1})'   # browse commits

git branch --all | sed 's/^[* ] //' | fzf \
  --preview 'git log --oneline --color=always {}' | xargs git switch            # fuzzy branch switch

git -c color.status=always status -s | fzf -m --ansi | awk '{print $2}' | xargs git add   # stage picks

f=$(git ls-files | fzf) && c=$(git log --oneline -- "$f" | fzf | cut -d' ' -f1) \
  && git checkout "$c" -- "$f"                                                   # restore file from a chosen commit
```

## Multi-select (`-m`) + `xargs` for bulk actions

```bash
rg -l 'TODO' | fzf -m --preview 'bat --color=always {}' | xargs $EDITOR   # Tab marks, Shift-Tab unmarks
```

## Pick-and-run pickers

```bash
jq -r '.scripts | keys[]' package.json | fzf | xargs -I{} npm run {}   # run an npm script

rg -oN --no-heading -r '$1' '^\s*def (test_\w+)' -tpy \
  | fzf --preview 'rg -n {} tests/' | xargs -I{} ./venv/bin/python -m pytest -k {} -q   # pick + run one test

ps -ef | fzf -m --header-lines=1 | awk '{print $2}' | xargs kill        # kill by fuzzy match
lsof -iTCP -sTCP:LISTEN -P -n | fzf --header-lines=1                    # which process holds a port
docker ps --format '{{.ID}}\t{{.Names}}\t{{.Image}}' | fzf | awk '{print $1}'   # container picker
```

## Make everything faster (shell rc)

```bash
export FZF_DEFAULT_COMMAND='rg --files --hidden -g "!.git"'   # powers Ctrl-T and bare `fzf`
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_DEFAULT_OPTS="--height 60% --layout=reverse --border --bind ctrl-/:toggle-preview"
```

Built-in keybindings once `fzf --zsh`/`--bash` is sourced: **Ctrl-T** (paste a file path),
**Ctrl-R** (fuzzy history), **Alt-C** (cd into a subdir).

## Gotchas

- `fzf` reads **stdin**; with no pipe it uses `$FZF_DEFAULT_COMMAND` (or walks the tree).
- Paths with spaces need `-0`/`xargs -0` upstream (e.g. `rg -l0 ... | xargs -0`).
- `become`/`reload` need fzf >= 0.38; check `fzf --version`.
