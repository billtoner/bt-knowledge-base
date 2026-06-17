# procs

A modern `ps`; colored output, tree view, search, and ports/containers built in.

## Use it

```bash
procs                                  # all processes, colorized columns
procs nginx                            # fuzzy filter by name/args
procs --tree                           # process tree
procs --sortd cpu                      # sort by CPU descending (or `mem`)
procs --watch                          # auto-refresh, top-like
```

## Notes

- Filters match command, args, PID, and user; numeric args also match ports
- Shows listening TCP/UDP ports and the Docker container per process by default
