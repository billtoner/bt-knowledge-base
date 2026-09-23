# sqlite-utils

CLI for SQLite by Simon Willison. Replaces "write a one-off Python script to query/dump/import"
with single commands.

**Tags:** database · sqlite · sql

## Cool features

- **Ad-hoc queries.** `sqlite-utils db.db "SELECT ..." --table` (or `--json`, `--csv`, `--nl`).
- **Schema dump.** `sqlite-utils schema db.db` prints CREATE TABLE statements for everything.
- **Tables list.** `sqlite-utils tables db.db --counts` — list with row counts.
- **Insert from JSON/CSV.** `sqlite-utils insert db.db mytable data.json` auto-creates the table
  and infers column types from the data.
- **Convert formats.** Pipe SQL output to JSON, CSV, plain, table, or even GeoJSON.
- **Search via FTS.** `sqlite-utils enable-fts db.db mytable col1 col2` adds full-text search.
- **Inspect history.** Hooks into FPOC's `insole_pressure_buffer.db` for ad-hoc data exploration.

## Useful in FPOC

```bash
# Where SQLite DB lives on Pi
DB=/audiopulse/insole_pressure_buffer.db

# Tables + counts
sqlite-utils tables $DB --counts

# Schema for a specific table
sqlite-utils schema $DB sessions

# Ad-hoc query, table output
sqlite-utils $DB "SELECT name, start_ts, end_ts FROM sessions ORDER BY start_ts DESC LIMIT 10" --table

# Same as JSON, pipe-friendly
sqlite-utils $DB "SELECT name, start_ts FROM sessions" --json

# Find all events for a session
sqlite-utils $DB "SELECT timestamp, event_type, data FROM events WHERE session_id = ? LIMIT 20" \
    -p '["p001_walk_20260516_1400"]' --table

# Count pressure rows per session — quick health check
sqlite-utils $DB "SELECT session_id, COUNT(*) FROM pressure_buffer GROUP BY session_id" --table

# Dump everything to CSVs for a participant
sqlite-utils $DB "SELECT * FROM sessions WHERE name LIKE 'p001_%'" --csv > p001-sessions.csv
sqlite-utils $DB "SELECT * FROM events   WHERE session_id LIKE 'p001_%'" --csv > p001-events.csv
```

## Killer one-liners

```bash
# What's the largest table?
sqlite-utils tables $DB --counts --json | jq -r '.[] | "\(.count)\t\(.table)"' | sort -rn | head

# Find recent events touching calibration
sqlite-utils $DB "SELECT timestamp, event_type FROM events WHERE event_type LIKE '%calibration%' ORDER BY timestamp DESC LIMIT 20" --table

# Show JSON event data nicely
sqlite-utils $DB "SELECT data FROM events WHERE event_type='session_qualification_summary' LIMIT 1" --json | jq .
```

## Install

```bash
brew install sqlite-utils       # already in Brewfile
# Or:
uv tool install sqlite-utils    # if you want a venv-isolated copy
```

## Vs. raw `sqlite3` CLI

`sqlite3 db.db "SELECT ..."` works for simple queries. `sqlite-utils` wins when you want:
- JSON/CSV output (not just text columns)
- Auto-infer schema from data
- Insert/import from JSON without writing CREATE TABLE
- Multi-step operations (enable FTS, add indexes, etc.) without remembering SQL syntax

For one-shot SELECT statements with simple text output, raw `sqlite3` is faster to type.

## Vs. DB Browser for SQLite

| Need | Tool |
|---|---|
| Pipeable output for scripts | sqlite-utils |
| Eyeball data in a spreadsheet view | DB Browser |
| One-off ad-hoc query | sqlite-utils |
| Edit a row manually | DB Browser |
| Schema design / visual relationships | DB Browser |
| CI / automation | sqlite-utils |
