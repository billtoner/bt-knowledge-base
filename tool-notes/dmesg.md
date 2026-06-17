# dmesg

Kernel ring buffer; boot, hardware, OOM-killer, and driver messages.

## Read it

```bash
dmesg -H                               # human timestamps + pager
dmesg -w                               # follow new messages live
dmesg -l err,warn                      # only errors and warnings
dmesg -T | grep -i -E 'oom|killed'     # OOM-killer events (absolute time)
```

## Notes

- `-H` adds colors + relative/human time; `-T` is absolute human time
- Often needs root (or `sysctl kernel.dmesg_restrict=0`)
- For messages that survive reboots: `journalctl -k -b -1` (previous boot)
