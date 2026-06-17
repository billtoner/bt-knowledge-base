# bq

BigQuery CLI — run queries, manage datasets/tables, and load or extract data.

## Querying

```bash
bq query --nouse_legacy_sql 'SELECT name, COUNT(*) c FROM `proj.ds.t` GROUP BY name ORDER BY c DESC LIMIT 10'
bq query --nouse_legacy_sql --format=prettyjson 'SELECT ...'   # JSON output
bq query --dry_run --nouse_legacy_sql 'SELECT ...'             # bytes-scanned estimate, no run
```

## Datasets & tables

```bash
bq ls                                      # datasets in the active project
bq ls proj:dataset                         # tables in a dataset
bq show --schema --format=prettyjson proj:ds.table   # table schema
bq mk --dataset --location=US proj:ds      # create a dataset
```

## Load & extract

```bash
bq load --autodetect --source_format=CSV ds.t gs://bucket/data.csv
bq load --source_format=NEWLINE_DELIMITED_JSON ds.t gs://bucket/data.json schema.json
bq extract ds.t gs://bucket/out-*.csv      # export a table to GCS
```

## Killer flags

- `--nouse_legacy_sql` — use standard SQL; set it on every query
- `--dry_run` — see bytes scanned (cost) before you run it
- `--format=csv|json|prettyjson|sparse` and `--max_rows=N`
- `--location` — dataset region (must match the data)
