# pre-commit

Manage and run git pre-commit hooks; this repo uses it for ruff, pytest, and
secret scanning.

## Setup & run

```bash
pre-commit install                     # register the git hook (once per clone)
pre-commit run --all-files             # run every hook over the whole repo
pre-commit run ruff-check --all-files  # run a single hook
pre-commit autoupdate                  # bump hook versions in the config
```

## Handy

```bash
SKIP=pytest git commit -m "wip"        # skip one hook for a single commit
pre-commit run --files a.py b.py       # only specific files
pre-commit clean                       # clear cached hook environments
```

## Notes

- Config lives in `.pre-commit-config.yaml`; each hook runs in an isolated env
- `SKIP=hook-id` (or `git commit --no-verify`) bypasses hooks when you must
