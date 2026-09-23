# ss

Modern replacement for `netstat`. Reads kernel socket info directly — instant on hosts where `netstat` crawls.

**Tags:** network

## Cool features

- **Built-in filter language.** `ss -t state established '( dport = :443 or dport = :80 )'` — no `grep`/`awk` pipeline needed.
- **`-K` closes sockets.** With root, you can forcibly tear down a stuck TCP connection without killing the owning process. Few people know this exists.
- **`-i` exposes live TCP internals.** `cwnd`, `rtt`, `retrans`, `pacing_rate` — gold for diagnosing slow connections that aren't actually dropped.

## What's listening, by process

```bash
sudo ss -tulpn                          # the everyday "what's bound to what"
                                        #   -t TCP, -u UDP, -l listening, -p process, -n numeric
sudo ss -ltn '( sport = :22 or sport = :443 )'   # narrow to specific ports
ss -lx                                  # listening Unix sockets — fast way to find a daemon's socket path
```

## Established connections — finding noisy peers

```bash
ss -tn state established | awk 'NR>1{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head
                                        # which remote IPs hold the most connections to this host?
sudo ss -tnp | awk -F'"' '/users:/{print $2}' | sort | uniq -c | sort -rn
                                        # which local processes hold the most TCP connections?
ss -tn '( dst 10.0.0.0/8 )'             # all TCP flowing into the 10/8 net
```

## Tearing down a stuck connection

```bash
sudo ss -K dst 192.0.2.7 dport = :6379  # kill our redis sockets to a flapping replica;
                                        # the owning process keeps running and just sees ECONNRESET
```

## Why is *that* connection slow?

```bash
ss -tin dst :443 | grep -A1 203.0.113.4 # live TCP metrics for a specific peer:
                                        # rtt, cwnd, retrans, lost, rcv_space
```

## Quick socket-state summary

```bash
ss -s                                   # one-shot counts: TCP estab, syn-sent, time-wait, etc.
```

## Habit shifts from netstat

| Old | New |
|---|---|
| `netstat -tulpn` | `sudo ss -tulpn` |
| `netstat -an \| grep ESTABLISHED` | `ss -tn state established` |
| `netstat -s` | `ss -s` |
| `netstat -i` | `ip -s link` (different tool, same intent) |

## Killer flags

- `-K` — close matched sockets (root; kernel 4.9+ / iproute2 4.2+)
- `-i` — TCP info (`cwnd`, `rtt`, `retrans`, `pacing_rate`, …)
- `-p` — show owning process (PID + comm)
- `-o` — show timers (`timer:(keepalive,...,N)`); useful for hung half-closed sockets
- `state X` — filter by `established`, `syn-sent`, `time-wait`, `closing`, `listening`, …
