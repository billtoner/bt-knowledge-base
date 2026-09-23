# mtr (My TraceRoute)

Continuous traceroute + ping in one screen. Watch where packets actually drop instead of inferring from a single traceroute run.

**Tags:** network · monitoring

## Cool features

- **`-T` for TCP probes.** When ICMP/UDP get filtered, TCP often gets through — try the port your real traffic uses.
- **`-r` report mode** gives a clean, paste-ready summary. The default interactive view does not.
- **`--json` / `--csv`** for automation.

## "Where is the packet loss?"

```bash
mtr -rwbz example.com                   # report, wide, both names+IPs, ASN per hop
                                        # exactly what to attach to a network ticket
mtr -c 100 -r example.com               # bounded — 100 cycles then exit
```

## When ICMP is blocked

```bash
mtr -T -P 443 example.com               # TCP probes to 443 — bypasses ICMP filtering
mtr -u -P 53 example.com                # UDP probes to 53 (DNS)
```

## High-resolution view of a flaky path

```bash
sudo mtr -i 0.1 example.com             # 100ms between probes; needs root
                                        # makes intermittent loss surface faster
```

## JSON for monitoring scripts

```bash
mtr --json -c 30 example.com | jq '.report.hubs[] | {host, Loss: ."Loss%", Avg}'
```

## Killer flags

- `-r` — report mode (non-interactive)
- `-w` — wide output (no truncation)
- `-b` — show both names and IPs
- `-z` — show ASN for each hop
- `-T` / `-u` — TCP / UDP probes (default is ICMP)
- `-P <port>` — destination port for TCP/UDP probes
- `-c N` — bounded run of N cycles, then exit
