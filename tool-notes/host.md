# host

Smaller, friendlier DNS lookup. When you don't need `dig`'s detail, `host` says the answer in one line.

**Tags:** dns · network

## Quick lookups

```bash
host example.com                                  # A + AAAA in one shot
host -t MX example.com                            # mail servers
host -t NS example.com                            # nameservers
host -t TXT example.com                           # SPF / DMARC / verification tokens
host -a example.com                               # all common record types (less detail than dig +trace)
```

## Query a specific resolver

```bash
host example.com 8.8.8.8                          # positional: domain, then resolver
host example.com 1.1.1.1
```

## Reverse lookup

```bash
host 1.1.1.1                                      # PTR record
host 2606:4700:4700::1111                         # works with IPv6 too
```

## Set a timeout / retry count

```bash
host -W 2 -R 1 example.com                        # 2s per query, retry once
                                                  # useful in scripts where you don't want to hang
```

## When to reach for dig instead

- You need `+trace` or `+nssearch`.
- You want to query authoritative servers directly with `@server`.
- You want raw, scriptable output (`+short`).
- You're debugging EDNS / DNSSEC / large responses.
