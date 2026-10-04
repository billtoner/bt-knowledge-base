# zsh-glob-gotchas

Two zsh globbing surprises that make `ls *.ext` fail in ways bash never would.

**Tags:** shell · zsh · globbing · gotcha

## A filename starting with `-` looks like a flag

When a glob **matches**, zsh expands it to the filenames *before* the command runs.
If a matched name starts with `-` (e.g. `- Training Guide.pdf`), `ls` parses it as an
option and bails — the glob worked fine, it's `ls` complaining:

```bash
ls *.pdf                # ls: invalid option -- '  (a leading "- " file got read as a flag)
```

Fixes:

```bash
ls -- *.pdf             # -- ends option parsing; everything after is a filename
ls ./*.pdf              # expands to ./-Training..., so no leading dash
```

## An unmatched glob is a hard error (`nomatch`)

zsh aborts the whole command when a glob matches nothing — the command never launches.
bash instead passes the pattern through literally.

```bash
ls *.dmg                # zsh: no matches found: *.dmg   (ls never ran)
                        # bash would run `ls *.dmg` → "No such file or directory"
```

Fixes:

```bash
setopt nonomatch        # global: pass unmatched globs through literally, bash-style
ls *.dmg(N)             # per-glob: (N) nullglob — expand to nothing instead of erroring
```

## Habit shifts from bash

| bash behavior | zsh behavior |
|---|---|
| unmatched glob passed through literally | `no matches found`, command aborts |
| `shopt -s nullglob` | `(N)` qualifier, or `setopt null_glob` |
| `shopt -s dotglob` | `(D)` qualifier, or `setopt glob_dots` |
