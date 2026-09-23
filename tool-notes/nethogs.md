# nethogs

`top` for network bandwidth, grouped **by process** rather than by flow. The answer to "*which* program is eating the link?"

**Tags:** network · monitoring · tui

## Quick start

```bash
sudo nethogs                                      # auto-pick the default interface
sudo nethogs eth0                                 # specific interface
sudo nethogs eth0 wlan0                           # multiple interfaces at once
```

## View tweaks

```bash
sudo nethogs -v 3                                 # cumulative bytes (not rate)
sudo nethogs -d 5                                 # 5-second refresh
sudo nethogs -t                                   # trace mode: no curses, parseable lines for scripts
```

## Interactive keys

- `m` — cycle units (KB/s, KB total, B/s, etc.)
- `s` — sort by sent
- `r` — sort by received
- `l` — toggle showing connection limits / all connections
- `q` — quit

## When to reach for iftop instead

`nethogs` is per-process; `iftop` is per-flow. If you want "show me *all* the connections this box is making and how much each is using," that's iftop.
