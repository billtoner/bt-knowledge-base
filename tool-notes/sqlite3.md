# sqlite3

Official SQLite CLI. Open a `.db`, explore the schema, run queries, import/export. Lightweight, no server.

**Tags:** database · sqlite · sql

## Cool features

- **Dot commands** (`.tables`, `.schema`, `.mode`, `.import`) are CLI conveniences — they're not SQL, they're meta.
- **One-shot mode**: `sqlite3 db.sqlite "SELECT ..."` runs and exits — perfect for scripts.
- **`.mode box` / `.mode markdown`** render results as nice tables in modern sqlite3 (≥ 3.33).
- **`.import` does CSV in one line** — no Python needed for "load this spreadsheet."
- **`PRAGMA foreign_keys = ON`** is *off by default*. Always turn it on if your schema uses FKs.
- **`EXPLAIN QUERY PLAN`** is the lightweight query analyzer — readable, fast.
- **`.dump`** outputs a full SQL recreate-from-scratch script — great for backup, diffs, or schema review.

## Open / setup the prompt

```bash
sqlite3 mydata.db                  # interactive
sqlite3                            # in-memory database (gone on exit)

# Useful inside the prompt — paste once, or put in ~/.sqliterc to persist
.headers on
.mode column                       # also: box, markdown, csv, json, tabs, line
.timer on                          # show elapsed for each query
.nullvalue NULL                    # render NULLs visibly
```

## Schema discovery

```sql
.tables                            -- list tables
.schema users                      -- CREATE statement for one table
.schema                            -- everything
.indexes users                     -- indexes on a table
.fullschema                        -- tables + indexes + triggers
PRAGMA table_info(users);          -- column details (name, type, NOT NULL, PK)
```

## Query

```sql
SELECT * FROM users LIMIT 10;
SELECT count(*) FROM users WHERE created_at > '2025-01-01';
```

## One-shot from the shell

```bash
sqlite3 mydata.db "SELECT count(*) FROM users;"          # quick count
sqlite3 -header -csv mydata.db "SELECT * FROM users;" > users.csv
sqlite3 mydata.db < script.sql                            # run a SQL file
sqlite3 mydata.db ".dump" > backup.sql                    # full backup
sqlite3 newdata.db < backup.sql                           # restore
```

## CSV import / export

```sql
.mode csv
.import users.csv users            -- load CSV into table "users" (creates if absent)
.mode csv
.headers on
.output users.csv
SELECT * FROM users;
.output stdout                     -- back to terminal
```

## Run a SQL script

```sql
.read setup.sql
.read migration_002.sql
```

## Pragmas worth knowing

```sql
PRAGMA foreign_keys = ON;          -- ENFORCE FK constraints (off by default!)
PRAGMA journal_mode = WAL;         -- better concurrency, persists
PRAGMA synchronous = NORMAL;       -- safe + faster than FULL
PRAGMA integrity_check;            -- verify DB consistency
PRAGMA quick_check;                -- faster, less thorough
PRAGMA page_size;                  -- inspect
PRAGMA optimize;                   -- update query planner stats
```

## Performance / planning

```sql
EXPLAIN QUERY PLAN
  SELECT * FROM orders o JOIN users u ON u.id = o.user_id
  WHERE u.email = 'x@y.com';

ANALYZE;                           -- rebuild stats so the planner is smarter
```

## Useful dot commands

- `.help` — list dot commands
- `.tables [pattern]` — match by glob
- `.schema [table]` — CREATE statement(s)
- `.dump [table]` — SQL to recreate DB or table
- `.read <file>` — run a SQL file
- `.import <csv> <table>` — load CSV
- `.mode <fmt>` — `column`, `box`, `markdown`, `csv`, `json`, `line`, `tabs`
- `.headers on|off`
- `.output <file>` — redirect to file; `.output stdout` to revert
- `.timer on|off`
- `.quit` — exit
