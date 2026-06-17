# awk

Field- and record-oriented text processing; the pattern-action workhorse.

## Fields & filters

```bash
awk '{print $2, $NF}' file             # 2nd field and the last field
awk -F: '{print $1}' /etc/passwd        # custom field separator
awk '$3 > 100' data                     # rows where column 3 > 100
awk 'NR==1 || $5=="ERROR"' log          # header line plus matching rows
```

## Aggregation

```bash
awk '{sum+=$1} END{print sum}' nums      # sum a column
awk '{a[$1]+=$2} END{for(k in a) print k, a[k]}' data   # group-by sum
awk 'NF && !seen[$0]++' file            # dedup, keep order, skip blank lines
```

## Reshape & format

```bash
awk -F, 'BEGIN{OFS="\t"} {$1=$1; print}' csv   # CSV -> TSV
awk '{printf "%-20s %s\n", $1, $2}' file        # aligned columns
```

## Notes

- `NR` record number, `NF` field count, `$0` whole line, `$N` field N
- `-F` input separator, `OFS` output separator; `BEGIN{}`/`END{}` run before/after
