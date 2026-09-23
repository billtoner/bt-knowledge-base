# jq

Command-line JSON processor. Filter, transform, and reshape JSON like `awk` for structured data.

**Tags:** json · data

## Cool features

- **Filter syntax is a tiny language.** `.foo.bar` navigates; `|` pipes filters; `[]` iterates arrays; `select(...)`, `map(...)`, `length`, `keys` cover most needs.
- **`-r` strips JSON quotes from string output** — essential when piping to other shell commands.
- **`-c` emits compact, one-object-per-line.** Turns a JSON array into NDJSON for streaming pipelines.
- **`--arg` and `--argjson`** pass shell variables into jq safely (no string-mashing).
- **String interpolation in output**: `"\(.first) \(.last)"` builds composite values inline.
- **Type inspection**: `type` returns `"string" | "number" | "array" | ...` — useful for branching with `if`.

## Extract a field

```bash
jq '.name' file.json                          # one field (quoted)
jq -r '.name' file.json                       # raw — no quotes, pipe-friendly
jq '.user.email' file.json                    # nested
jq '.user.email // "none"' file.json          # default if null/missing
jq '.users[0]' file.json                      # first array element
jq '.users[-1]' file.json                     # last
jq '.users[2:5]' file.json                    # slice
```

## Iterate over arrays

```bash
jq '.[]' file.json                            # one object per output line (after -c)
jq '.users[] | .name' file.json               # field of each
jq -r '.users[] | .name' file.json | sort -u  # unique names, piped to sort
```

## Filter — `select`

```bash
jq '.users[] | select(.age > 30)' file.json
jq '.users[] | select(.status == "active") | .id' file.json
jq '.users[] | select(.tags | contains(["admin"]))' file.json
jq '.users[] | select(.email | test("@example\\.com$"))' file.json   # regex
```

## Transform — `map`, object construction

```bash
jq 'map(.name)' file.json                          # array of just names
jq '[.users[] | .name]' file.json                  # same, alternative syntax
jq 'map({id, name})' file.json                     # pick fields (shorthand)
jq '[.users[] | {id, full: "\(.first) \(.last)"}]' file.json
jq '[.users[] | {(.id|tostring): .name}] | add' file.json   # id → name map
```

## Inspect structure

```bash
jq 'keys' file.json                           # top-level keys
jq 'length' file.json                         # array/object length
jq '.users | length' file.json                # length of a sub-array
jq 'paths(.. | scalars)' file.json            # every leaf path (deep inspect)
jq 'type' file.json                           # "object" / "array" / ...
```

## Output formats

```bash
jq -c '.users[]' file.json                    # compact, one-line — NDJSON pipeline
jq -r '.users[].name' file.json               # raw strings (no quotes)
jq -j '.users[].name' file.json               # joined (no newlines)
jq --tab '.' file.json                        # tab-indent instead of 2-space
```

## Pass shell variables safely

```bash
threshold=30
jq --argjson t "$threshold" '.users[] | select(.age > $t)' file.json

name="alice"
jq --arg n "$name" '.users[] | select(.name == $n)' file.json
```

## Pipelines

```bash
curl -s https://api.example.com/users | jq '.[] | .id'
aws ec2 describe-instances | \
    jq -r '.Reservations[].Instances[] | "\(.InstanceId)\t\(.State.Name)\t\(.Tags[]?|select(.Key=="Name")|.Value)"'
docker inspect $CID | jq '.[0].NetworkSettings.IPAddress'
```

## Multiple files / streaming

```bash
jq '.' file1.json file2.json                  # process multiple files in sequence
jq -s 'add' a.json b.json                     # --slurp: read all as one array, then merge
cat *.json | jq -c '.'                        # validate/compact stream
```

## Killer flags

- `-r` — raw string output (no quotes)
- `-c` — compact (NDJSON)
- `-s` — slurp all inputs into one array
- `-j` — join output (no trailing newlines)
- `--arg <name> <str>` / `--argjson <name> <json>` — pass shell vars in safely
- `-e` — exit non-zero if output is null/false (great for shell guards)
