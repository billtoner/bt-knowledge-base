# iperf3

Active throughput measurement between two hosts. "Is the network actually slow, or is it the app?"

**Tags:** network · monitoring

## Cool features

- **`-R` reverses direction** without swapping which side runs the server. Test download with the same setup.
- **`--bidir`** runs upstream and downstream simultaneously — a different result from running each direction back-to-back.
- **`-J` emits JSON** with everything (retransmits, cwnd snapshots, CPU usage).

## Server side

```bash
iperf3 -s                               # listen on default port 5201
iperf3 -s -D                            # daemonize
iperf3 -s -p 5202                       # alt port (e.g., to run two on one box)
```

## Standard client tests

```bash
iperf3 -c server.example.com -t 30                  # 30-second TCP test
iperf3 -c server.example.com -t 30 -P 8             # 8 parallel streams (saturate a fat pipe)
iperf3 -c server.example.com -t 30 -R               # reverse: measure download instead
iperf3 -c server.example.com -t 30 --bidir          # simultaneous up + down
```

## UDP + loss / jitter

```bash
iperf3 -c server.example.com -u -b 100M             # push UDP at 100 Mbps target
                                                    # output includes jitter + lost packets
iperf3 -c server.example.com -u -b 0                # no rate cap — "how much UDP can you take?"
```

## Capture results for analysis

```bash
iperf3 -c server.example.com -t 60 -i 1 -J > run.json
                                                    # JSON, 1s intervals, 60s total
jq '.intervals[].sum.bits_per_second' run.json | numfmt --to=iec --suffix=bps
                                                    # per-interval throughput, human-readable
```

## Killer flags

- `-t N` — test duration (default 10s is usually too short)
- `-P N` — parallel streams
- `-R` — reverse (server → client)
- `--bidir` — both directions at once
- `-u` — UDP mode
- `-b RATE` — target bitrate for UDP; `0` = unlimited
- `-J` — JSON output
- `-i N` — report every N seconds
- `-O N` — omit first N seconds (skip TCP slow-start warmup)
