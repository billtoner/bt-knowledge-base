# yq

YAML/JSON/XML processor with jq-style syntax. Edit YAML files **preserving comments** — the killer feature over generic JSON tooling.

> Two implementations exist: **mikefarah/yq** (Go; default on Homebrew) and **kislyuk/yq** (Python wrapper around jq). They have different syntax. This note covers mikefarah's (`yq --version` → `mikefarah/yq` if you have the common one).

**Tags:** yaml · json · data

## Cool features

- **Same operations work on YAML, JSON, and XML.** `-o=json`, `-p=xml`, etc. flip the format.
- **`-i` modifies files in place.** Preserves YAML comments, anchors, and key order. No more "round-tripped through Python and lost everything."
- **`eval-all`** processes multiple files together — needed for merges, multi-doc operations.
- **Multi-doc YAML** (Kubernetes manifests) is first-class: `.. | select(...)` recurses across docs.
- **`strenv()`** reads shell env vars safely, no string concat.

## Read fields

```bash
yq '.spec.replicas' deployment.yaml
yq '.metadata.name' deployment.yaml                       # quoted string
yq '.metadata.name' deployment.yaml -r                    # raw (no quotes)
yq '.users[]' users.yaml                                  # iterate array
yq '.users[].email' users.yaml                            # field of each
yq '.users[] | select(.role == "admin") | .email' users.yaml
```

## Update values

```bash
yq '.spec.replicas = 5' deployment.yaml                   # prints modified
yq -i '.spec.replicas = 5' deployment.yaml                # write back in place
yq -i '.image = strenv(IMG)' deployment.yaml              # IMG=foo:1.2 yq -i ...

# Update all matching across nested structures
yq -i '(.. | select(has("image")).image) = "myimg:latest"' manifest.yaml
```

## Add / delete

```bash
yq -i '.spec.env += [{"name": "DEBUG", "value": "1"}]' deployment.yaml
yq -i 'del(.metadata.annotations)' deployment.yaml
yq -i 'del(.users[] | select(.disabled))' users.yaml
```

## Multi-doc YAML (Kubernetes)

```bash
yq '. | select(.kind == "Service")' manifest.yaml         # extract one doc kind
yq 'select(.kind == "Deployment").spec.replicas = 5' manifest.yaml
yq '[.metadata.name]' manifest.yaml                       # name from each doc (as array)
yq '.kind' manifest.yaml                                  # list all doc kinds
```

## Format conversion

```bash
yq -o=json file.yaml                                      # YAML → JSON
yq -o=json -I=0 file.yaml                                 # JSON, no indentation
yq -p=json -o=yaml file.json                              # JSON → YAML
yq -p=xml -o=yaml file.xml                                # XML → YAML
yq -o=props file.yaml                                     # → java properties
```

## Merge / patch (eval-all)

```bash
# Deep-merge two files (file 1 wins on conflicts)
yq eval-all '. as $item ireduce ({}; . * $item)' base.yaml overlay.yaml

# Simple merge (mikefarah's * operator)
yq eval-all 'select(fi == 0) * select(fi == 1)' base.yaml overlay.yaml
```

## Common kubectl pipeline tricks

```bash
kubectl get deploy -o yaml | yq '.items[] | .metadata.name + " " + (.spec.replicas|tostring)'
kubectl get -o yaml deploy app | yq -i '.spec.replicas = 3' -    # edit via stdin (- = stdin)
```

## Killer flags

- `-i` — in-place modification (preserves comments + order)
- `-r` — raw string output (no quotes)
- `-o=<fmt>` — output: `yaml`, `json`, `props`, `xml`
- `-p=<fmt>` — input parser (autodetect by ext, override here)
- `-I=N` — indentation (0 = compact JSON)
- `strenv(NAME)` — pull an env var safely
- `eval-all` — operate on multiple files together (merges, multi-input)
