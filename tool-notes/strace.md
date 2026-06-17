# strace

Trace the system calls and signals of a process — the first stop for "what is
it actually doing / why is it stuck".

## Attach or launch

```bash
strace -f -e trace=openat,read,write ./prog   # follow forks, filter to syscalls
strace -f -p 12345                     # attach to a running process (+ children)
strace -c ./prog                       # summary table: time/calls/errors per syscall
```

## Common investigations

```bash
strace -f -e trace=network curl https://example.com   # just network syscalls
strace -e trace=file -y ./prog         # file ops, with resolved fd paths
strace -tt -T ./prog                   # wall-clock timestamps + time per call
strace -f -o trace.log ./prog          # log to a file, keep stdout clean
```

## Killer flags

- `-f` — follow child processes (you almost always want this)
- `-e trace=GROUP` — `file`/`network`/`process`/`signal`/`memory`, or a syscall list
- `-c` — syscall summary; `-p PID` — attach; `-y` — decode fds to paths
- `-s 256` — show longer string arguments

## Notes

- `ltrace` is the library-call analogue; `strace -k` adds stack traces
