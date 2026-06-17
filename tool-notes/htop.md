# htop

Interactive process and resource monitor (htop; btop for a richer UI).

## Launch with a filter

```bash
htop                                   # interactive process/CPU/mem viewer
htop -u toner                          # only one user's processes
htop -p $(pgrep -d, nginx)             # only specific PIDs
htop -t                                # start in tree view
```

## In-TUI keys

- `F6` or `<` `>` — change sort column; `F5` tree view; `H` toggle threads
- `F3` search, `F4` incremental filter, `F9` kill (choose the signal)
- `u` filter by user, `F2` setup (meters, colors, columns)

## Notes

- `btop` is the modern alternative: graphs, mouse, disk/net meters, themes
- Per-core meters and the load/mem/swap header are configurable in F2 setup
