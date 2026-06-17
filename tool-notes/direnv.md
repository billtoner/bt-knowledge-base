# direnv

Per-directory environment variables, auto-loaded when you `cd` in.

## Use it

```bash
direnv allow                           # trust this dir's .envrc (after reviewing it)
direnv reload                          # re-evaluate the current .envrc
direnv edit .                          # edit + allow in one step
direnv status                          # what's loaded, and from where
```

## .envrc recipes (put these in .envrc)

```bash
export DATABASE_URL=postgres://localhost/dev   # plain env var
dotenv                                          # load a .env file
layout python3                                  # auto-create/activate a venv
use flake                                       # nix flake devshell
```

## Notes

- Re-run `direnv allow` after any .envrc change — it runs shell code, so it asks
- Needs the shell hook: `eval "$(direnv hook zsh)"` in `~/.zshrc`
