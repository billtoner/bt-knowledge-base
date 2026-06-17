# sar

Historical and live system stats — sysstat's `sar`, plus `dstat` for a live
combined view.

## Live sampling (interval count)

```bash
sar 2 5                                # CPU: 5 samples, 2s apart
sar -r 2 5                             # memory utilization
sar -d -p 2 5                          # per-disk activity (friendly names)
sar -n DEV 2 5                         # per-NIC throughput
```

## Historical (from the daily archive)

```bash
sar -q                                 # run queue + load averages, today
sar -f /var/log/sysstat/sa15 -u        # CPU from the 15th
sar -s 09:00:00 -e 10:00:00 -u         # a specific window
```

## dstat (live, combined)

```bash
dstat -tcmnd                           # time, cpu, mem, net, disk in one row
dstat --top-cpu --top-io               # busiest process per resource
```

## Notes

- `sar` reads archives written by the sysstat collector — enable its service
- `dstat` is the at-a-glance live dashboard across resources
