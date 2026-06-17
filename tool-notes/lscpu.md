# lscpu

CPU architecture, topology, caches, and instruction-set flags.

## Use it

```bash
lscpu                                  # sockets, cores, threads, caches, flags
lscpu -e                               # per-CPU table (core/socket/NUMA mapping)
lscpu -J                               # JSON output
lscpu | grep -i -E 'vmx|svm'           # hardware virtualization present?
```

## Notes

- Threads-per-core > 1 means SMT / hyper-threading is enabled
- `flags` lists ISA extensions (avx2, aes, sha_ni, …); `-e` shows the NUMA layout
