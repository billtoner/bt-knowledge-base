# just

A modern command runner; like make, but for tasks (not file builds).

## Everyday

```bash
just                                   # run the default recipe
just --list                            # list recipes with their doc comments
just build                             # run a recipe
just deploy prod                       # recipe with arguments
just --choose                          # fuzzy-pick a recipe (needs fzf)
```

## Authoring (justfile)

```bash
just --show deploy                     # print one recipe's source
just --evaluate                        # show variable values
just --fmt --unstable                  # format the justfile
```

## Notes

- No tab/space pitfalls; recipes can be sh/bash/python/etc. via a `#!` shebang
- `set dotenv-load`, parameters, and recipe dependencies make it a sane make-for-tasks
