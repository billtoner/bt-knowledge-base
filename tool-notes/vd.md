# vd (VisiData)

TUI spreadsheet for tabular data. Opens CSV, TSV, JSON, JSONL, SQLite, Parquet, Excel, HTML tables, fixed-width — and lets you sort, filter, pivot, group, and re-save in any format. The "I just need to look at this CSV" tool.

**Tags:** data · csv · tui

## Cool features

- **One viewer for everything.** Same keystrokes whether the input is `.csv`, `.json`, `.parquet`, `.db`, or a remote URL.
- **Auto type-inference.** Numeric, date, currency columns are detected — sort and aggregate "just work."
- **Frequency tables in one keystroke.** `F` on a column → counts + percentages, sorted desc.
- **Pivot tables in one keystroke.** `W` groups by current column and summarizes another.
- **`--play` macros.** Recorded keystrokes save to a `.vd` file you can replay on new data — repeatable, scriptable.
- **Saves back out in any supported format.** Open `.csv`, manipulate, save as `.json` or `.sqlite`.

## Open something

```bash
vd data.csv
vd data.json
vd data.sqlite                       # browses tables, then drill into one
vd data.parquet
vd big.csv.gz                        # transparently decompresses
vd https://example.com/data.csv      # remote URLs (read-only)
vd file1.csv file2.csv               # multiple sheets — '[' to switch
```

## Movement (vim-ish)

| Keys | What |
|---|---|
| `h j k l` / arrows | move cell |
| `gg` / `G` | top / bottom |
| `zh` / `zl` | scroll columns left/right |
| `Ctrl-D` / `Ctrl-U` | half-page down/up |
| `/pattern` | search current column (`n` next, `N` prev) |
| `g/pattern` | search all columns |

## Columns

| Keys | What |
|---|---|
| `-` | hide column under cursor |
| `gv` | unhide all |
| `^` | rename column |
| `#` | set type: numeric (int) |
| `%` | set type: float |
| `$` | set type: currency |
| `@` | set type: date |
| `~` | set type: string (reset) |
| `=` | add derived column (Python expression: e.g. `price * qty`) |

## Rows

| Keys | What |
|---|---|
| `s` / `u` | select / unselect row |
| `gs` / `gu` | select / unselect all |
| `,` | select rows matching current cell value |
| `\|` | select rows matching regex on current column |
| `z\|` | keep only selected rows |
| `z\\` | drop selected rows |
| `d` | delete row(s) |

## Sort / filter / stats

| Keys | What |
|---|---|
| `[` / `]` | sort asc / desc on current column |
| `F` | **frequency table** for current column |
| `I` | describe column (count/min/max/mean) |
| `W` | **pivot table** — group by current col, summarize another |
| `gW` | melt / unpivot |

## Save / export

| Keys | What |
|---|---|
| `Ctrl-S` | save current sheet (format from extension) |
| `gCtrl-S` | save all sheets |
| `Ctrl-Q` | quit; `gq` quits everything |

## Replay macros (batch mode)

```bash
# Record: do work in vd, save keystrokes with Ctrl-D to workflow.vd
# Replay on new data without opening the UI:
vd --play workflow.vd --batch data.csv
vd --play workflow.vd --batch data.csv -o cleaned.csv
```

## Common recipes

```bash
# Peek at a CSV — better than `column -t` + less
vd data.csv

# Look at one table of a SQLite DB without leaving the terminal
vd app.db

# Convert formats
vd data.csv          # then Ctrl-S → data.json
vd data.parquet      # then Ctrl-S → data.csv

# Frequency / top-N
vd access.log.csv    # cursor to a column, press F

# Pivot
vd sales.csv         # cursor to "region", press W, choose "amount" + "sum"
```

## Habit shifts

| Task | vd | Alternative |
|---|---|---|
| Peek at a CSV | `vd file.csv` | `column -t -s, file.csv \| less -S` |
| Frequency by column | `F` in vd | `awk -F, '{print $3}' \| sort \| uniq -c \| sort -rn` |
| Pivot / group | `W` in vd | pandas, SQL, mlr |
| CSV → JSON | open in vd, `Ctrl-S` `data.json` | `csvkit`, `mlr`, `jq` |
| SQLite table peek | `vd db.sqlite` | `sqlite3 db.sqlite '.mode column'` |

## Killer flags

- `--play <macro.vd>` — replay a recorded workflow
- `--batch` — non-interactive (with `--play`)
- `-o <file>` — write output (with `--play --batch`)
- `-f <format>` — force input format when extension isn't enough
