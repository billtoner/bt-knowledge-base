# nft (nftables)

The modern replacement for `iptables`/`ip6tables`/`arptables`/`ebtables`. One unified CLI, atomic rule loads, native sets and maps, JSON output.

**Tags:** firewall · network

## Cool features

- **Named sets** (`@blocklist`) let you add/remove IPs from a rule without rewriting the rule. With `flags interval` they coalesce CIDRs efficiently.
- **`nft -f file.nft`** loads a ruleset atomically — no half-applied state if a single rule fails.
- **`nft monitor`** streams every ruleset change live. Great for seeing what an installer or daemon is doing behind your back.

## Show what's loaded

```bash
sudo nft list ruleset                             # everything, as restorable nft commands
sudo nft list table inet filter                   # one table
sudo nft -j list ruleset                          # JSON output for scripts
```

## Bootstrap a baseline ruleset

```bash
sudo nft add table inet filter
sudo nft add chain inet filter input \
    '{ type filter hook input priority 0; policy drop; }'
sudo nft add chain inet filter forward \
    '{ type filter hook forward priority 0; policy drop; }'

sudo nft add rule inet filter input iif lo accept
sudo nft add rule inet filter input ct state established,related accept
sudo nft add rule inet filter input tcp dport { 22, 80, 443 } accept
sudo nft add rule inet filter input ip protocol icmp icmp type echo-request accept
```

## Sets — the killer feature

```bash
sudo nft add set inet filter blocklist '{ type ipv4_addr; flags interval; }'
sudo nft add element inet filter blocklist '{ 192.0.2.0/24, 198.51.100.7 }'
sudo nft add rule inet filter input ip saddr @blocklist drop

# Add / remove without rewriting the rule:
sudo nft add element inet filter blocklist '{ 203.0.113.5 }'
sudo nft delete element inet filter blocklist '{ 203.0.113.5 }'
```

## NAT

```bash
sudo nft add table ip nat
sudo nft add chain ip nat prerouting  '{ type nat hook prerouting  priority -100; }'
sudo nft add chain ip nat postrouting '{ type nat hook postrouting priority  100; }'

# Port redirect 80 → 8080
sudo nft add rule ip nat prerouting tcp dport 80 redirect to 8080

# Masquerade outbound
sudo nft add rule ip nat postrouting oif eth0 masquerade
```

## Atomic loads / persistence

```bash
sudo nft list ruleset > /etc/nftables.conf
sudo nft -f /etc/nftables.conf                    # atomic — all-or-nothing
sudo systemctl enable --now nftables              # restore on boot (Debian/Ubuntu)
```

## Watch what's happening

```bash
sudo nft monitor                                  # live ruleset changes
sudo nft monitor trace                            # packet-level (needs `meta nftrace set 1` on a rule)
```

## Habit shifts from iptables

| Old (`iptables`) | New (`nft`) |
|---|---|
| `iptables -L -v -n` | `nft list ruleset` |
| `iptables -A INPUT -p tcp --dport 22 -j ACCEPT` | `nft add rule inet filter input tcp dport 22 accept` |
| `iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080` | `nft add rule ip nat prerouting tcp dport 80 redirect to 8080` |
| `iptables-save > rules.v4` / `iptables-restore < rules.v4` | `nft list ruleset > rules.nft` / `nft -f rules.nft` |
| Multiple commands to rate-limit | `nft add rule … limit rate 3/minute accept` |

## Killer pieces

- `inet` family — single rule applies to both v4 and v6
- `{ a, b, c }` anonymous sets — multiple values inline
- Named sets / maps — mutable membership without rule rewrites
- `nft -j` — JSON output for scripts
- `nft monitor` — live ruleset/event stream
