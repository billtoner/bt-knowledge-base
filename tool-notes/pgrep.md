# pgrep

Find and signal processes by name or attributes (pgrep, pkill).

## Find

```bash
pgrep -a nginx                         # matching PIDs + full command line
pgrep -u toner -l ssh                  # by user, list process names
pgrep -f 'python.*worker'              # match against the whole arg string
pgrep -n java                          # the newest matching process
```

## Signal

```bash
pkill -f 'python.*worker'              # signal by full-command match
pkill -HUP nginx                       # send a specific signal (here: reload)
pkill -u olduser                       # every process owned by a user
```

## Notes

- `-f` matches the entire command line, not just the process name
- `pgrep -d,` joins PIDs with commas — e.g. `htop -p $(pgrep -d, nginx)`
- Always dry-run a `pkill -f` pattern with `pgrep -f` first
