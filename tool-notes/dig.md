# dig

DNS debugging: query specific servers, walk the resolution chain, get the raw record types `host` won't show you.

**Tags:** dns · network

## Cool features

- **`+trace` walks from the root.** Catches misconfigured glue, lame delegations, and "my recursive resolver is caching a stale answer."
- **`@server` aims at a specific resolver or authoritative.** Lets you bypass your local DNS entirely.
- **`+short` cuts the noise.** Pipe-friendly answer-only output for scripting.

## Quick lookups

```bash
dig +short example.com                  # just the A records
dig +short MX example.com               # just the MX hosts
dig -x 1.1.1.1 +short                   # reverse DNS
dig +noall +answer example.com any      # every record type, no chrome
```

## "Is my DNS wrong?" — compare resolvers

```bash
dig @1.1.1.1 +short example.com         # what Cloudflare DNS says
dig @8.8.8.8 +short example.com         # what Google DNS says
dig +short example.com                  # what your configured resolver says
                                        # mismatch = something between you and the truth is stale
```

## Trace resolution from the root

```bash
dig +trace example.com                  # walk root → TLD → authoritative
                                        # the last block is the authoritative answer
```

## Authoritative spelunking

```bash
dig @ns1.example.com example.com SOA    # SOA serial straight from the source
dig +nssearch example.com               # query every NS, compare SOA serials
                                        # detects replicas that haven't caught up
dig CHAOS TXT version.bind @ns1.example.com   # fingerprint the DNS server software
```

## Killer flags

- `+short` — answer-only, scriptable
- `+trace` — recursive walk from root
- `+nssearch` — query every NS, compare serials
- `+noall +answer` — strip headers/auth/additional; keep the answers
- `+tcp` — force TCP (test EDNS / large-response handling)
- `-x` — reverse lookup (PTR)
