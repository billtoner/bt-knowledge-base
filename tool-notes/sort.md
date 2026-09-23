# sort

Sort lines of text. The combination of `-u`, `-n`, `-h`, `-k`, and `-t` covers 99% of real use.

**Tags:** text

## Cool features

- **`-u` is sort + dedupe in one pass.** Faster than `sort | uniq`.
- **`-h` understands human sizes.** `1K`, `2M`, `3G` sort correctly — pairs perfectly with `du -h`.
- **`-V` is version sort.** `1.2.10` comes after `1.2.2`, not before. Use it for tag lists, semver, kernel versions.
- **`-R` is shuffle.** Random reorder; same line never duplicated. (`-r` is reverse — easy to confuse.)
- **`-k F,F` is half-open, not full-line.** `sort -k3` sorts from field 3 to end of line; `sort -k3,3` sorts on field 3 only. The latter is almost always what you want.
- **`-s` is stable.** Preserves original order on ties — important when chaining sorts.
- **`LC_ALL=C` makes sort *fast*** and predictable (byte-wise, no locale rules). Worth it for big files.

## Basic

```bash
sort file.txt                              # ascending alphabetic
sort -r file.txt                           # reverse
sort -u file.txt                           # unique + sort (faster than | uniq)
```

## Numeric / human / version

```bash
sort -n file.txt                           # numeric
sort -h file.txt                           # human sizes (1K, 2M, 3G)
sort -V file.txt                           # version sort (1.2.10 > 1.2.2)
sort -g file.txt                           # general numeric (handles 1e5 scientific notation)
```

## By column

```bash
sort -k2 file.txt                          # from field 2 to end of line
sort -k2,2 file.txt                        # field 2 only
sort -k3,3 -n file.txt                     # field 3, numerically
sort -t: -k3,3 -n /etc/passwd              # custom separator (colon)
sort -k1,1 -k3,3 -n file.txt               # multi-key: by 1st, then 3rd numeric
```

## Reverse + numeric / human (rank biggest first)

```bash
du -h /var/log/* | sort -hr | head         # biggest log dirs first
ps -eo pid,rss,cmd | sort -k2 -nr | head   # top memory hogs (RSS in KB)
```

## Shuffle / random

```bash
sort -R file.txt                           # random order
shuf file.txt                              # same idea, GNU's dedicated tool
```

## Pair with `uniq -c` for frequency counts

```bash
sort access.log | uniq -c | sort -rn | head -10        # top 10 most-frequent lines
cut -d' ' -f1 access.log | sort | uniq -c | sort -rn   # top IPs
```

## Stable sort (preserve ties)

```bash
sort -s -k1,1 file.txt                     # stable: rows with equal field 1 keep original order
```

## Large files / performance

```bash
LC_ALL=C sort huge.txt                     # bytewise locale — 2-3x faster
sort --parallel=8 -S 2G huge.txt           # 8 threads, 2 GB buffer
sort -T /fast/tmp huge.txt                 # use a specific tmp dir (when /tmp is small)
```

## Reverse a sort key without flipping the whole line

```bash
sort -k1,1 -k2,2nr file.txt                # field 1 asc, field 2 numeric desc (per-key reverse)
```

## Killer flags

- `-u` — sort + dedupe
- `-n` — numeric; `-h` — human sizes; `-V` — version; `-g` — general numeric (scientific)
- `-r` — reverse
- `-k F[,F]` — sort by field (use `F,F` to limit, not from-F-to-end)
- `-t <char>` — field separator (default: whitespace runs)
- `-s` — stable
- `-R` — random shuffle
- `--parallel=N` / `-S <size>` / `-T <dir>` — performance knobs for big files
