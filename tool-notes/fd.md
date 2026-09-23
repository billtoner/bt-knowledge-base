# fd

Replacement for `find`. Smart-case, gitignore-aware, parallel exec.

**Tags:** search · files

## Cool features

- **`fd pattern`** — regex search on filenames, recursive, smart-case, respects `.gitignore`.
- **Extension filter.** `fd -e py` for all `.py`. Can repeat: `fd -e py -e pyi`.
- **Type filter.** `-t f` (files), `-t d` (dirs), `-t l` (symlinks).
- **Parallel exec — the killer feature.** `fd -e py -x ruff check {}` runs the command on every match, in parallel. Use `-X` (capital) to invoke once with all paths (xargs-style).
- **Time filters.** `fd --changed-within 1week`, `--changed-within 1day`, even `--changed-before 1month`.
- **Size filters.** `fd -S +1M` (>1MB), `fd -S -10k` (<10KB).
- **Glob mode.** `fd -g '*.json' config/` — glob syntax instead of regex when you want it.
- **Override the gitignore opt-in.** `-I` includes gitignored files; `-H` includes hidden files.

## Useful in FPOC

```bash
fd -e py audiopulse/calibration            # all Python in calibration/
fd -t f test_ tests/                       # all test_* files
fd -e py --changed-within 1day             # recently-edited Python
fd -e log -S +1M                            # logs bigger than 1MB
fd -e py audiopulse/ble -x ruff check       # lint only BLE files
fd -t d __pycache__ -x rm -rf               # purge all __pycache__ dirs
fd -e py -x wc -l | sort -rn | head         # 10 biggest Python files
```

## Exec placeholders (`-x` per-file, `-X` batched)

`{}` full path · `{.}` no extension · `{/}` basename · `{//}` parent dir · `{/.}` basename-no-ext.

```bash
fd -e png -x cwebp {} -o {.}.webp     # convert each png -> webp (runs in PARALLEL)
fd -e pyc -X rm                       # ONE rm call with all matches (batched)
fd -t f -x chmod 644 {}               # normalize file perms
fd -e pdf 'copy' -x sh -c 'mv "$1" "${1/ copy/}"' _ {}   # bulk rename: strip a " copy" suffix
```

## Seeing what's normally hidden, and scoping

```bash
fd -u pattern                  # -u == -H -I (unrestricted: hidden + gitignored)
fd --full-path 'src/.*/test'   # match against the whole path, not just the name
fd -d 2 -t d                   # max depth 2
fd --min-depth 2 pattern
```

## Time & size filters

```bash
fd --changed-within 2days             # edited in the last 2 days
fd --changed-before 2weeks -e log     # old logs
fd --size +10M                        # bigger than 10 MB  (long form of -S +10M)
fd --size -1k -t f                    # tiny files
```

## Safe pipelines & clever combos

```bash
fd -0 -e log | xargs -0 rm            # null-delimited -> survives spaces in names
fd -e py | xargs wc -l | sort -n      # LOC per file
fd -t d -u __pycache__ -X rm -rf      # delete every __pycache__ in the tree
fd -e js | fzf --preview 'bat --color=always {}' | xargs $EDITOR   # find + preview + open
fd --changed-within 1day -t f -E node_modules -E .git              # what did I touch today?
```

## Setup

```bash
export FZF_DEFAULT_COMMAND='fd --type f --hidden --exclude .git'   # power fzf's file walk
```

## Habit shifts from find

| Old | New |
|---|---|
| `find . -name "*.py"` | `fd -e py` |
| `find . -name "foo*"` | `fd foo` |
| `find . -newer file` | `fd --changed-within 1week` |
| `find . -type d -name node_modules -exec rm -rf {} +` | `fd -t d node_modules -x rm -rf` |

## Killer flags

- `-x` — parallel exec on each match
- `-X` — single exec with all matches (xargs-style)
- `-e ext` — extension filter
- `-t f` / `-t d` — type filter
- `--prune` — don't descend into matches
