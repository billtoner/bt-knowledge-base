# uv

Fast Python project, dependency, and environment manager (the one this repo's
kb tool is installed with).

## Projects & dependencies

```bash
uv init myproj                         # new project (pyproject.toml)
uv add httpx 'fastapi>=0.110'          # add deps, update the lockfile
uv remove httpx
uv sync                                # install exactly what's locked
uv lock --upgrade                      # refresh the lockfile
```

## Run & tools

```bash
uv run pytest                          # run in the project env (auto-synced first)
uvx ruff check .                       # run a tool without installing it (like pipx)
uv tool install ruff                   # persistent tool install
```

## Python & venv

```bash
uv python install 3.12                 # manage interpreters
uv venv                                # create .venv
uv pip install -r requirements.txt     # pip-compatible interface
```

## Notes

- Replaces pip / pip-tools / venv / pyenv / pipx for most workflows, and is fast
- `uv run` keeps the environment in sync with the lockfile automatically
