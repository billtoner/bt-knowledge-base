# traceroute

Classic per-hop probe of a network path. Useful when you need a single snapshot (vs `mtr`'s continuous view) or when a path differs depending on protocol.

**Tags:** network

## Cool features

- **`-T` uses TCP probes.** Many firewalls drop UDP/ICMP traceroute but pass TCP to your real ports. Probe the path your traffic actually takes.
- **`--mtu`** discovers the path MTU as it traces. Finds the hop where fragmentation kicks in.
- **`-q 1`** sends one probe per hop instead of three — faster, and often enough.

## Common runs

```bash
traceroute -n example.com                         # no DNS lookups; faster, less noisy
traceroute -q 1 example.com                       # one probe per hop
traceroute -m 30 example.com                      # cap at 30 hops (default is 30; raise for far paths)
```

## When ICMP/UDP is filtered

```bash
sudo traceroute -T -p 443 example.com             # TCP to 443 — bypasses ICMP filtering
sudo traceroute -I example.com                    # ICMP echo probes (Windows-style)
traceroute -U -p 53 example.com                   # explicit UDP/53
```

## Path MTU discovery

```bash
sudo traceroute --mtu example.com                 # shows MTU at each hop
sudo traceroute -F -s 192.168.1.5 example.com     # set DF flag and source IP
```

## Source-routed test from a specific NIC

```bash
sudo traceroute -i eth1 -s 10.0.0.5 example.com   # force a specific outgoing interface + source
```

## Killer flags

- `-n` — no DNS
- `-q N` — N probes per hop
- `-m N` — max hops
- `-T` — TCP probes (root)
- `-I` — ICMP echo probes (root)
- `-U` — UDP probes (default on Linux; non-root)
- `-p PORT` — destination port
- `-F` — set Don't Fragment
- `--mtu` — show path MTU

## See also

`mtr` for the continuous, packet-loss-per-hop view of the same data.
