# gron

Make JSON greppable. Flattens JSON into one assignment per line — `json.users[0].name = "alice";` — so you can find every value with its full path using `grep`. Reversible: `gron -u` rebuilds JSON from the flat form.

**Tags:** json · text

## Cool features

- **Every value gets a unique path** that's both human-readable and grep-friendly.
- **Reversible.** `gron file.json | grep something | gron -u` reconstructs valid JSON containing just the matched paths.
- **Sortable** — `gron a.json | sort` and `gron b.json | sort` are diffable line-by-line.
- **No filter language to learn.** Unlike jq, gron only needs the tools you already know — `grep`, `awk`, `sort`, `diff`.
- **Great for unfamiliar APIs.** When you don't know the shape, `gron | less` is faster than guessing jq paths.

## Basic

```bash
gron file.json
# json.users = [];
# json.users[0] = {};
# json.users[0].name = "alice";
# json.users[0].age = 30;
# json.users[1].name = "bob";

gron file.json | grep email                       # every "email" anywhere in the doc
gron file.json | grep -E "name|email"
```

## Reverse — `gron -u` (ungron)

```bash
# Grep + reassemble valid JSON containing just the matched paths
gron file.json | grep email | gron -u

# Filter to one user and rebuild
gron file.json | grep '^json\.users\[2\]' | gron -u
```

## Diff two JSON files structurally

```bash
diff <(gron a.json | sort) <(gron b.json | sort)
# Cleaner than diffing pretty-printed JSON — order-independent, path-aware.
```

## Explore an unknown API response

```bash
curl -s https://api.github.com/users/torvalds | gron | less
curl -s https://api.example.com/things | gron | grep -i price
```

## NDJSON / streaming

```bash
gron --stream file.ndjson                         # each input line is its own JSON doc
kubectl logs --tail=100 -f pod | jq -c '.' | gron --stream | grep err
```

## Habit shifts — gron vs jq

| Task | gron | jq |
|---|---|---|
| Explore unfamiliar JSON | `gron \| less` | guess paths, iterate |
| Grep for a value/key by path | `gron \| grep` | `paths(..) \| select(...)` |
| Filter + transform | not its job | jq's home turf |
| Diff two JSON files | `diff <(gron a\|sort) <(gron b\|sort)` | needs careful normalization |
| Pluck a few paths and rebuild | `gron \| grep \| gron -u` | jq projection |

## Killer flags

- `-u` / `--ungron` — reverse mode (rebuild JSON)
- `--stream` — NDJSON input
- `-j` / `--json` — emit JSON lines instead of gron syntax (alternate flat form)
- `-c` / `--colorize` — color the output (key in one color, value in another)
- `-s` / `--sort` — sort keys before output (deterministic for diffing)
