# doggo

Modern, colorized `dig`; JSON output, DoH/DoT, and multi-resolver comparison.

## Lookups

```bash
doggo example.com                      # A/AAAA, colorized
doggo MX example.com                   # a specific record type
doggo example.com @1.1.1.1             # query a specific resolver
doggo example.com @https://dns.google/dns-query   # DNS-over-HTTPS
```

## Output & comparison

```bash
doggo --json example.com | jq          # machine-readable
doggo A example.com @1.1.1.1 @8.8.8.8  # compare resolvers side by side
doggo --short example.com              # just the answers
```

## Notes

- Speaks DoH/DoT/DNSCrypt — handy when plain UDP/53 is filtered
- `--json` is scriptable where `dig` needs `+short` and manual parsing
