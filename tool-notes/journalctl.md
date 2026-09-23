# journalctl

Query the systemd journal. Structured logs filterable by unit, time, boot, priority, and arbitrary metadata fields.

**Tags:** logs · systemd

## Cool features

- **Time ranges accept natural language.** `--since "1 hour ago"`, `--since yesterday --until today`.
- **`-b -N` shows logs from previous boots.** `journalctl -b -1` is the last boot — invaluable post-crash forensics.
- **Structured fields are filterable.** Every entry has metadata (`_PID`, `_UID`, `_SYSTEMD_UNIT`, `_TRANSPORT`) — filter on any of them like a key=value lookup.
- **JSON output** for machine parsing. `-o json-pretty` shows the full record, every field journald captured.
- **`-p` accepts a range.** `-p warning..err`, not just a floor.
- **Vacuum by time or size.** `--vacuum-time=7d` drops older entries; `--vacuum-size=500M` caps total disk usage.

## Logs for one unit

```bash
journalctl -u nginx                         # all entries
journalctl -u nginx -f                      # follow (like tail -f)
journalctl -u nginx -n 200                  # last 200 lines
journalctl -u nginx -e                      # jump to end (paged)
```

## Time ranges

```bash
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx --since today
journalctl -u nginx --since "2026-05-15 09:00" --until "2026-05-15 10:00"
journalctl -u nginx --since yesterday --until today
```

## Boots

```bash
journalctl --list-boots                     # index of recent boots
journalctl -b                               # current boot only
journalctl -b -1                            # previous boot (post-crash forensics)
journalctl -k                               # kernel ring buffer, persistent (dmesg-like)
```

## Severity

```bash
journalctl -p err                           # err and above (err, crit, alert, emerg)
journalctl -p warning..err -u nginx         # range of priorities
```

## Output formats

```bash
journalctl -u nginx -o cat                  # message only — clean for grep
journalctl -u nginx -o json-pretty          # full structured record
journalctl -u nginx -o short-iso            # ISO-8601 timestamps
```

## Filter by structured fields

```bash
journalctl _PID=1234
journalctl _UID=1000 --since today
journalctl _SYSTEMD_UNIT=nginx.service _TRANSPORT=stdout
journalctl --field _SYSTEMD_UNIT            # list all values for a field
```

## Disk usage & retention

```bash
journalctl --disk-usage
sudo journalctl --vacuum-time=7d            # drop entries older than 7 days
sudo journalctl --vacuum-size=500M          # cap journal at 500 MB
journalctl --verify                         # checksum-verify the journal files
```

## Killer flags

- `-u <unit>` — filter to one unit
- `-f` — follow
- `-b -N` — Nth previous boot
- `-p <level>` — priority filter (accepts ranges)
- `-o <format>` — output format (`cat`, `short-iso`, `json`, `json-pretty`)
