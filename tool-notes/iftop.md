# iftop

`top`, but for network connections. "Which flows are eating my bandwidth right now?"

**Tags:** network · monitoring · tui

## Quick start

```bash
sudo iftop -i eth0                                # bandwidth by connection on eth0
sudo iftop -i eth0 -P                             # show ports too
sudo iftop -n -P -B                               # no DNS, ports shown, BYTES (not bits)
```

## Filter to a subnet or pcap filter

```bash
sudo iftop -i eth0 -F 192.168.1.0/24              # only flows involving this subnet
sudo iftop -i eth0 -f 'port 443'                  # pcap filter — any normal tcpdump expression works
```

## Interactive keys (while it's running)

- `n` — toggle DNS lookups
- `p` — toggle port display
- `P` — pause display (lets you read the screen)
- `t` — cycle line layouts (combined / split / per-direction)
- `T` — toggle cumulative-bytes column
- `s` / `d` — toggle showing source / destination host
- `S` / `D` — toggle source / destination port
- `b` — toggle the bottom bar graph
- `B` — cycle between bps / Bps / packets-per-second

## When to reach for nethogs instead

`iftop` shows flows (host pairs); `nethogs` shows processes. If you want "*which* process is downloading X," that's nethogs.
