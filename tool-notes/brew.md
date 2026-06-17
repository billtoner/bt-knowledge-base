# brew

Homebrew package manager for macOS/Linux; formulae, casks, services.

## Install / upgrade

```bash
brew install ripgrep fd                 # formulae (CLI tools)
brew install --cask rectangle           # casks (GUI apps, macOS)
brew upgrade                            # upgrade everything outdated
brew outdated                           # preview what would upgrade
```

## Inspect & maintain

```bash
brew info ripgrep                       # versions, deps, caveats
brew deps --tree ffmpeg                 # dependency tree
brew cleanup                            # remove old versions and caches
brew doctor                             # diagnose a broken install
```

## Services & Brewfile

```bash
brew services list                      # background services (start/stop/restart)
brew bundle dump                        # write a Brewfile of what's installed
brew bundle --file=Brewfile             # reinstall everything from a Brewfile
```

## Notes

- `brew bundle` makes a machine's toolset reproducible — commit the Brewfile
