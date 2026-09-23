# DB Browser for SQLite

GUI for SQLite. The "double-click and eyeball the data" tool. Free, cross-platform, mature.

**Tags:** database · sqlite · gui

## Cool features

- **Browse Data tab** — opens any table as a spreadsheet-like view. Sort columns, filter, edit cells inline.
- **Execute SQL tab** — write multi-line queries, see results in a results pane. Auto-completes
  table/column names from the schema. Saves query history.
- **Database Structure tab** — visual view of tables, indexes, views, triggers. Click any to see CREATE statement.
- **Visual schema editing** — add/drop columns, change types via dialogs (modifies underlying CREATE).
- **Export** — to CSV / SQL / JSON via menu. Easier than figuring out the right `.mode csv` / `.output` incantations.
- **Plot** — built-in basic charting from query results (useful for eyeball pressure time-series).
- **No-install pure SQLite** — uses bundled SQLite library, no system dep on the SQLite version.

## Useful in FPOC

The natural workflow:
1. `scp pi@audiopulse-2:/audiopulse/insole_pressure_buffer.db ~/Desktop/today.db`
2. Open in DB Browser
3. Browse `pressure_buffer` — sort by timestamp, filter by session, visually scan
4. "Why does this session have 800 alerts and that one have 80?" — eyeball the events table
5. "Is the heel/toe ratio correct?" — write a query, plot the result

## When DB Browser beats sqlite-utils CLI

- You want to **see** all 16 sensor columns side-by-side
- You want to **scroll** through 50K rows looking for outliers
- You're **exploring** without knowing what query you want yet
- You want to **edit** a row to fix a bad migration
- You want a **quick chart** without breaking out matplotlib

## When sqlite-utils CLI beats DB Browser

- You're scripting / piping results
- You know the query
- The DB lives on a server you can't easily SCP from
- You want JSON output for further tooling

## A few keyboard shortcuts worth knowing

| Shortcut | Action |
|---|---|
| Cmd-O | Open database |
| Cmd-Enter | Execute SQL (in SQL tab) |
| Cmd-F | Find in current tab |
| Cmd-T | New SQL tab |

## Install

```bash
brew install --cask db-browser-for-sqlite
```

Already in your Brewfile.

## Gotchas

- **Opens databases read-write by default.** If you don't want to accidentally edit production
  data while exploring, use File → Open Read Only, or work on a copied file.
- **Doesn't show the WAL file by default.** If you have a busy SQLite DB (WAL mode) you may
  see stale data. Either copy the DB + `-wal` + `-shm` files together, or use sqlite-utils
  which handles WAL transparently.
- **Large tables are slow to render.** For tables with millions of rows, use Filter to scope
  what's shown — DB Browser tries to load all rows into the view by default.

## Quick workflow for FPOC pressure data

```bash
# 1. Snapshot from Pi
scp pi@audiopulse-2:/audiopulse/insole_pressure_buffer.db ~/Desktop/insole-snapshot.db

# 2. Open in DB Browser (or double-click in Finder)
open -a "DB Browser for SQLite" ~/Desktop/insole-snapshot.db

# 3. Browse Data → sessions table → most recent session
# 4. Use that session's name to filter pressure_buffer:
#    Browse Data → pressure_buffer → Filter on session_id column

# 5. Execute SQL → plot pressure over time for one sensor:
#    SELECT timestamp, sensor_value
#    FROM pressure_buffer
#    WHERE session_id = 'p001_walk_20260516_1400'
#      AND sensor_index = 0
#    ORDER BY timestamp
#    LIMIT 1000;
#    Then click Plot → choose timestamp as X, sensor_value as Y
```
