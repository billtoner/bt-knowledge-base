# nmap

Port scanning, host discovery, service identification. Use on networks you own or have explicit permission to scan.

**Tags:** network · security

## Cool features

- **NSE scripts** (`--script`) run Lua tests for vulns, brute-force, banner enumeration, TLS introspection — far beyond port discovery.
- **`-oA` saves three formats at once** (normal, XML, grepable). Future-you revisiting an old scan will thank present-you.
- **`-Pn`** skips host discovery. Useful when ICMP/ARP are blocked and you already know the host is up.

## Host discovery (no port scan)

```bash
sudo nmap -sn 192.168.1.0/24            # who's up? ARP + ICMP + a few probes
sudo nmap -PE -sn 192.168.1.0/24        # ICMP echo only (useful across L3 boundaries)
```

## Common port scans

```bash
sudo nmap -sS -T4 -F target             # SYN scan, fast timing, 100 most common ports
nmap -p- -T4 target                     # all 65535 TCP ports
nmap -p 80,443,8080-8090 target         # specific ports / ranges
sudo nmap -sU --top-ports 50 target     # 50 most common UDP ports (slow)
```

## Service version + default scripts

```bash
sudo nmap -sV -sC -p 22,80,443 target   # version detection + safe default scripts
sudo nmap -O target                     # OS fingerprint
```

## Find hosts with a specific port open

```bash
nmap -p 22 --open 10.0.0.0/24                       # only print hosts with 22 open
nmap -p 443 --open --script ssl-cert 10.0.0.0/24    # plus dump cert subject/issuer/expiry
```

## NSE scripts worth knowing

```bash
nmap --script vuln target                           # common vuln checks
nmap --script ssl-enum-ciphers -p 443 target        # TLS cipher support matrix
nmap --script http-title -p 80,443 10.0.0.0/24      # quick web-server recon
```

## Save everything

```bash
sudo nmap -sS -sV -oA scans/target target           # writes target.nmap, .xml, .gnmap
```

## Killer flags

- `-sS` — SYN (half-open) scan; needs root
- `-sV` — service / version detection
- `-sC` — run default scripts
- `-O` — OS fingerprinting
- `-T0`..`-T5` — timing template (0 paranoid → 5 insane)
- `-p-` — all 65535 ports
- `--top-ports N` — N most common ports
- `-Pn` — skip host discovery
- `--open` — only print hosts with at least one open port
- `-oA prefix` — save normal / XML / grepable outputs
