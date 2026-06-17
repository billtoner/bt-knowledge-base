# pipx

Install Python CLI apps in isolated virtualenvs (how this repo's `kb` is installed).

## Install / run

```bash
pipx install ruff                       # install a CLI in its own venv, on PATH
pipx install --force ./my-project       # (re)install from a local project
pipx run cowsay moo                     # run a tool once without installing
pipx list                               # installed apps + their venvs
```

## Maintain

```bash
pipx upgrade ruff                       # upgrade one app
pipx upgrade-all                        # upgrade everything
pipx inject powerline-status psutil     # add a library into an app's venv
pipx ensurepath                         # ensure ~/.local/bin is on PATH
```

## Notes

- Each app gets its own venv — no dependency conflicts between CLIs
- `pipx install --force <path>` is exactly what `kbinit` runs to (re)install this kb
