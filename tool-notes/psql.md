# psql

The PostgreSQL client; meta-commands, scripting, COPY, and EXPLAIN.

## Connect & run

```bash
psql "postgresql://user@host:5432/db"  # connection URI
psql -h host -U user -d db             # discrete flags
psql -d db -c 'SELECT version();'      # run one query and exit
psql -d db -f script.sql               # run a SQL file
```

## Meta-commands (inside psql)

- `\l` databases · `\dn` schemas · `\du` roles
- `\dt` list tables · `\d table` describe · `\df` functions
- `\x` toggle expanded rows · `\timing` show query times
- `\copy (SELECT ...) TO 'out.csv' CSV HEADER` — client-side export

## Performance

```bash
psql -d db -c 'EXPLAIN (ANALYZE, BUFFERS) SELECT ...'   # real plan + timing
```

## Notes

- `\x` makes wide rows readable; `\copy` runs client-side (no server file perms)
- Defaults in `~/.psqlrc`; non-interactive auth via `~/.pgpass` / `PGPASSWORD`
