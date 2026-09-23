# ripgrep (`rg`)

Replacement for `grep -r`. Faster, smarter defaults, gitignore-aware.

**Tags:** search · text · files · modern-unix

## Cool features

- **Recursive by default.** `rg pattern` already does what `grep -r pattern .` does.
- **Smart case** — lowercase pattern is case-insensitive; mixed-case is sensitive. No flag dance.
- **Respects `.gitignore`.** Doesn't waste time on `.venv/`, `__pycache__/`, build artifacts.
- **Type-aware filtering.** `rg "TODO" -t py` scans only Python files. See `rg --type-list` for the full taxonomy.
- **File-list output.** `rg -l "pattern"` lists files only — pipe to anything: `rg -l "boto3" | xargs code`.
- **Context windows.** `-C 3` shows 3 lines before/after each match; `-A` after only, `-B` before only.
- **Multiline regex.** `-U` flag lets your pattern span lines: `rg -U "def __init__\(.*\n.*ble_utils"`.
- **Inverse match.** `rg --files-without-match '"""' audiopulse/` — files missing a docstring.
- **Stats summary.** `--stats` adds match-count totals at the end.
- **Replace preview.** `rg "old" -r "new"` shows what the replacement would look like (read-only).

## Useful in FPOC

```bash
rg "assert .* is not None" audiopulse/     # find the pyright-fix asserts
rg "Optional\[" audiopulse/                # places where None is allowed
rg "TODO|FIXME|XXX" -t py                  # outstanding work markers
rg '@self\.app\.route'                      # Flask routes
rg -l "boto3" -t py                         # files that talk to DynamoDB
rg --stats "import sqlite3"                 # how widespread is sqlite usage?
rg -C 2 "compute_session_score"             # function uses with surrounding context
```

## Recursion & what gets searched

`rg` recurses from `.` by default — no recursion flag. `-r` means `--replace`, NOT recursive
(that's a grep-ism). If a search "misses" files, it's almost always `.gitignore`/hidden filtering.

```bash
rg foo                 # recursive from .  (== grep -r foo .)
rg foo a.js b.py       # named files only (non-recursive)
rg foo --hidden        # include dotfiles, still honor .gitignore
rg foo -uu             # ALSO search .gitignored + hidden (-u stacks: -uuu adds binary)
rg foo -g '!**/node_modules/**'   # recurse but prune a subtree
rg foo --max-depth 2   # limit descent
```

## Extraction (`-o` + `-r` capture replace) — rg as a mini sed/awk

`-N` no line numbers, `-I` no filename, `-o` only-match, `-r '$1'` emit the group.

```bash
rg -oNI --no-heading -r '$1' "os\.environ(?:\.get)?\(['\"]([A-Z_]+)" -tpy | sort -u   # env vars read
rg -oNI -r '$1' "from ['\"]([^'\"]+)['\"]" -tjs | sort | uniq -c | sort -rn           # import sources, counted
rg -oNI -r '$1' 'TODO\(([^)]+)\)' | sort | uniq -c | sort -rn                          # TODO owners, tallied
```

## PCRE2: lookarounds & backreferences (`-P`)

The default engine is fast but can't do these; `-P` switches to PCRE2.

```bash
rg -P '\b(\w+)\s+\1\b'              # doubled words: "the the"
rg -P '^(?!\s*//).*console\.log'   # console.log NOT on a comment line
rg -P 'fetch\((?!.*catch)'         # fetch calls with no catch on the line
```

## Multiline (`-U`) — match across line breaks

```bash
rg -U --multiline-dotall 'function (\w+)\([^)]*\)\s*\{[^}]*localStorage'   # signature + body
rg -U 'catch\s*\([^)]*\)\s*\{\s*\}'                                        # empty catch blocks (bug smell)
```

## Counting & surveying

```bash
rg -c 'def ' -tpy               # per-file function counts
rg --count-matches 'setTimeout' -tjs   # total occurrences (not files)
rg --stats 'TODO'               # matches / files / lines-searched summary
rg -w exit -tpy                 # -w = whole word (won't hit "exiting")
```

## Search only what changed (dirty tree / pre-commit)

```bash
git diff --name-only -z | xargs -0 rg -n 'console\.log|debugger'
rg -n 'FIXME' $(git diff --name-only origin/main)
```

## Preview & bulk-edit (safe, null-delimited)

```bash
rg --passthru -N 'practicimo' -r 'fretsy' practicimo.py | diff practicimo.py -   # preview a replacement
rg -l0 'oldName' | xargs -0 sed -i '' 's/oldName/newName/g'                       # -0 survives spaces in paths
rg --type-add 'web:*.{js,ts,css,html}' -tweb 'fretsy'                            # define + use a type on the fly
```

## Habit shifts from grep

| Old | New |
|---|---|
| `grep -rn "x" .` | `rg x` |
| `grep -i "x" .` | `rg x` (smart-case handles it) |
| `find . -name "*.py" -exec grep "x" {} \;` | `rg x -t py` |

## Killer flags

- `-l` — files with matches only
- `-w` — whole-word only
- `-g '!tests/'` — glob exclude (with `!`)
- `--hidden` — search hidden files
- `-uu` — also bypass `.gitignore` (use sparingly)
