# whois

Lookup tool for domain registration and IP ownership. Underrated for incident triage — "who owns this IP that's hitting me?"

**Tags:** network · dns

## Domain registration

```bash
whois example.com                                 # registrar, expiry, name servers, abuse contact
whois example.co.uk                               # ccTLDs work too; output format differs per registry
```

## IP ownership and AS info

```bash
whois 8.8.8.8                                     # who owns this IP block?
whois AS15169                                     # AS name + contacts (Google here)
```

## Team Cymru bulk-whois (ASN + CIDR for an IP)

```bash
whois -h whois.cymru.com " -v 8.8.8.8"            # one-line "what ASN and prefix is this?"
                                                  # the leading space inside quotes is required
```

Output: `AS | IP | BGP Prefix | CC | Registry | Allocated | AS Name` — perfect for tagging log lines.

## Bulk lookups via Team Cymru

```bash
# Many IPs at once, no client install:
{ echo begin; echo verbose; cat ips.txt; echo end; } | nc whois.cymru.com 43
                                                  # plain TCP whois; pipes whole list and gets ASN/CIDR for each
```

## IANA root / TLD info

```bash
whois -h whois.iana.org example.com               # which whois server is authoritative for the TLD?
                                                  # follow up with `whois -h <that server> example.com`
```

## Killer flags

- `-h HOST` — query a specific whois server (e.g. cymru, IANA, RIPE, ARIN)
- `-H` — suppress legal disclaimer boilerplate
- `--verbose` — show what's happening between you and the registry
