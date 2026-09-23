# ngrep

`grep` for network packets. Match a regex against payload bytes flying by on the wire.

**Tags:** network · packets

## Cool features

- **Matches on payload, not headers.** `ngrep 'User-Agent: curl' port 80` finds HTTP traffic by content — a thing `tcpdump` makes painful.
- **`-W byline`** prints payloads one line per packet — readable for HTTP/Redis/IRC/SMTP traffic.
- **Pcap filter is the same syntax as tcpdump.** Combine "what payload" with "what flow."

## Find HTTP requests

```bash
sudo ngrep -d any 'GET ' tcp port 80              # all HTTP GETs (note trailing space)
sudo ngrep -d any -W byline 'Host:' port 80       # who's hitting which Host header?
sudo ngrep -d any -i 'user-agent: curl' port 80   # case-insensitive — find curl traffic
```

## Catch cleartext secrets (auditing your own traffic)

```bash
sudo ngrep -d any -W byline -i 'password=|token=' port 80
                                                  # form posts and query strings
sudo ngrep -d any -W byline 'Authorization:' port 80
                                                  # cleartext bearer tokens / basic auth
```

## DNS payloads

```bash
sudo ngrep -d any '.' udp port 53                 # all DNS — '.' matches any byte
sudo ngrep -d any -q -W byline 'example\.com' port 53
                                                  # who's looking up this domain?
```

## Save matching packets

```bash
sudo ngrep -d any -O cap.pcap 'pattern' port 443
                                                  # writes only matched packets — small pcap, focused signal
```

## Killer flags

- `-d IFACE` — interface (`any` on Linux)
- `-W byline` — line-per-packet payload
- `-q` — quiet (only print matches, no `#`/`T` dots)
- `-i` — case-insensitive
- `-t` / `-T` — absolute / delta timestamps
- `-O FILE` — write matched packets to pcap
- pcap filter after the regex (e.g. `tcp port 80`)
