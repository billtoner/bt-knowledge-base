# qsv

Fast CSV toolkit; slice, stats, join, frequency, and search — a CSV swiss army knife.

## Look around

```bash
qsv headers data.csv                    # column names + indexes
qsv stats data.csv                      # type, min/max/mean/stddev per column
qsv frequency -s region data.csv        # value counts for a column
qsv sample 10 data.csv                  # random rows
```

## Slice & filter

```bash
qsv select region,amount data.csv       # pick/reorder columns
qsv search -s email '@example\.com' data.csv   # regex filter on a column
qsv sort -s amount -N data.csv          # numeric sort
qsv slice -s 0 -e 100 data.csv          # first 100 rows
```

## Join & reshape

```bash
qsv join id a.csv id b.csv              # inner join on a key column
qsv cat columns a.csv b.csv             # paste columns side by side
qsv tojsonl data.csv                    # CSV -> JSON Lines
```

## Notes

- Operations stream and are multithreaded — handles files larger than RAM
- `qsv stats`/`frequency` are the fastest way to understand an unknown CSV
