# perf

Linux perf; hardware counters, sampling profiles, and flame-graph-ready output.

## Quick counters & live profile

```bash
perf stat ./prog                       # cycles, instructions, cache misses, IPC
perf stat -p 12345 sleep 5             # counters for a running PID over 5s
perf top                               # live, system-wide hottest functions
```

## Record & report

```bash
perf record -g ./prog                  # sample with call graphs
perf record -g -p 12345 -- sleep 10    # sample a running process for 10s
perf report                            # interactive symbol/cost browser
perf script                            # raw samples (pipe into FlameGraph)
```

## Notes

- Needs access: check `sysctl kernel.perf_event_paranoid` (lower = more allowed)
- `-g` (or `--call-graph dwarf`) captures stacks; pair with Brendan Gregg's FlameGraph
- Target events directly: `perf stat -e cache-misses,branch-misses ./prog`
