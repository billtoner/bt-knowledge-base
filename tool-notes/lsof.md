# lsof

List open files — and since everything on Unix is a file, that means the
processes behind ports, sockets, locked mounts, and deleted-but-still-held files.

## Cool features

- **`-a` ANDs your filters.** Multiple selectors are OR by default; `-a` turns them into AND, so you can ask "network files *of this PID*".
- **`+L1` finds the disk leak.** Files with link count 0 are deleted but still open — the classic "`df` says full, `du` says it isn't" culprit.
- **`-t` prints bare PIDs**, made for piping straight into `kill`.

## What's using a port

```bash
lsof -i :3000                        # who's listening on / connected to port 3000
lsof -iTCP -sTCP:LISTEN -P -n        # every listening TCP socket, numeric & fast
lsof -i :8080 -t                     # just the PID(s):  kill $(lsof -i :8080 -t)
lsof -i @192.168.1.50                # connections to/from a specific host
```

## Files a process has open

```bash
lsof -p 12345                        # every file, socket, and FD held by PID 12345
lsof -c nginx                        # open files for all processes named nginx
lsof -i -a -p 12345                  # AND filters: only the network files of PID 12345
```

## What's holding a file or mount

```bash
lsof /var/log/syslog                 # which processes have this file open
lsof +D ~/project                    # everything open under a directory (recursive)
lsof /mnt/usb                        # "umount: target is busy" — find who's using it
```

## Deleted-but-open files (disk not freeing)

```bash
lsof +L1                             # link count < 1: deleted files still held open
lsof -nP +L1 | grep deleted          # the "df full but du clean" offender
```

## By user

```bash
lsof -u toner                        # all files opened by a user
lsof -u^root                         # everything NOT owned by root (^ negates)
```

## Killer flags

- `-i` — network files: `-i :PORT`, `-iTCP`, `-i @host`
- `-p PID` / `-c name` — restrict to a process by id or command name
- `-a` — AND the selectors together (default is OR)
- `-t` — terse: PIDs only, for piping into `kill`
- `-n -P` — skip host/port name resolution (much faster)
- `+L1` — deleted files still open; `+D dir` — recurse a directory
