# apt

Debian/Ubuntu package management (apt for humans, dpkg for low-level queries).

## Install / update / remove

```bash
sudo apt update                         # refresh package lists
sudo apt upgrade                        # upgrade installed packages
sudo apt install ripgrep fd-find        # install
sudo apt remove --purge some-pkg        # remove package + its config
sudo apt autoremove                     # drop orphaned dependencies
```

## Search & inspect

```bash
apt search rust                         # search the index
apt show ripgrep                        # version, deps, description
apt-cache policy ripgrep                # candidate vs installed version
```

## dpkg (low-level)

```bash
dpkg -l 'pattern*'                      # list matching installed packages
dpkg -L ripgrep                         # files a package installed
dpkg -S /usr/bin/rg                     # which package owns a file
sudo dpkg -i ./local.deb                # install a local .deb
```

## Notes

- `apt` is the friendly CLI; use `apt-get`/`apt-cache` in scripts (stable output)
