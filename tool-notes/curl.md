# curl

Transfer data over a URL — HTTP, HTTPS, FTP, and a dozen others. The de facto HTTP client.

**Tags:** http · download · network

## Cool features

- **`-L` follows redirects.** It's off by default — get used to typing it.
- **`-w '<format>'`** prints timing/size/code variables in a custom format — `%{http_code}`, `%{time_total}`, `%{size_download}`, etc.
- **`--resolve host:port:ip`** overrides DNS for one request — perfect for testing a service before it has DNS.
- **`-F field=@file`** does multipart file upload without thinking about `Content-Type` boundaries.
- **`-OJ`** uses the server's `Content-Disposition` filename — handy for downloads where the URL doesn't have a good name.
- **URL globbing** is built in: `curl -O 'https://x.com/file[1-5].zip'` downloads five files.
- **`--compressed`** sends `Accept-Encoding: gzip` and decompresses — visible speedup on large JSON.

## Basic GET

```bash
curl https://example.com                          # body only
curl -L https://example.com                       # follow redirects (almost always wanted)
curl -i https://example.com                       # include response headers
curl -I https://example.com                       # HEAD — headers only
curl -s https://example.com                       # silent (no progress bar)
curl -sS https://example.com                      # silent but still show errors
```

## Headers

```bash
curl -H 'Accept: application/json' https://api.example.com/things
curl -H "Authorization: Bearer $TOKEN" https://api.example.com/me
curl -H 'X-Trace-Id: abc-123' -H 'X-Source: ci' https://api.example.com/x   # repeat freely
```

## POST / PUT / PATCH / DELETE

```bash
# JSON
curl -X POST -H 'Content-Type: application/json' \
     -d '{"name": "alice"}' \
     https://api.example.com/users

# Body from file
curl -X PUT --data-binary @payload.json \
     -H 'Content-Type: application/json' \
     https://api.example.com/things/1

# Body from stdin
echo '{"a": 1}' | curl -X POST --data-binary @- \
                       -H 'Content-Type: application/json' \
                       https://api.example.com/things

# URL-encoded form
curl -d 'user=alice&pass=foo' https://api.example.com/login

# Delete
curl -X DELETE -H "Authorization: Bearer $TOKEN" https://api.example.com/things/1
```

## Multipart upload

```bash
curl -F 'file=@./report.pdf' -F 'title=April report' https://api.example.com/upload
curl -F 'file=@./report.pdf;type=application/pdf' https://api.example.com/upload
curl -F 'json=<./meta.json;type=application/json' \
     -F 'file=@./blob.bin' \
     https://api.example.com/upload
```

## Authentication

```bash
curl -u user:pass https://api.example.com         # basic auth
curl -u user: https://api.example.com             # prompts for password
curl -H "Authorization: Bearer $TOKEN" https://api.example.com
curl --netrc https://example.com                  # use ~/.netrc credentials
```

## Save the response body

```bash
curl -o output.html https://example.com           # specific filename
curl -O https://example.com/file.zip              # use URL's filename
curl -OJ https://example.com/d/abc                # use Content-Disposition filename
curl -O https://example.com/file[1-5].zip         # URL globbing — five files
```

## Test a service without proper DNS

```bash
# Pretend foo.example.com resolves to 10.0.0.5 just for this call
curl --resolve foo.example.com:443:10.0.0.5 https://foo.example.com

# Connect to a different host:port but keep the original Host header
curl --connect-to foo.example.com:443:internal-lb:443 https://foo.example.com
```

## Bypass cert validation (testing only)

```bash
curl -k https://self-signed.example.com           # don't verify TLS cert
```

## Debug / inspect

```bash
curl -v https://example.com                       # request + response headers
curl -vv https://example.com                      # + TLS handshake details
curl --trace-ascii - https://example.com          # full wire trace
curl --trace-time -v https://example.com          # add timestamps to -v output
```

## Custom timing format (powerful)

```bash
curl -w 'HTTP %{http_code} in %{time_total}s\n' -s -o /dev/null https://example.com

# Full timing breakdown
curl -w '
dns=%{time_namelookup}
connect=%{time_connect}
ssl=%{time_appconnect}
ttfb=%{time_starttransfer}
total=%{time_total}
' -s -o /dev/null https://example.com
```

## Reliability

```bash
curl --max-time 10 --connect-timeout 3 https://example.com
curl --retry 3 --retry-delay 2 https://flaky.example.com
curl --retry 5 --retry-all-errors https://flaky.example.com   # retry on 4xx/5xx too
```

## Compressed responses

```bash
curl --compressed https://api.example.com         # sends Accept-Encoding, decompresses
```

## Cookies / sessions

```bash
curl -c cookies.txt -b cookies.txt https://example.com/login -d 'u=x&p=y'
curl -b cookies.txt https://example.com/me        # reuse jar on subsequent calls
```

## Quick "is the service up?"

```bash
curl -fsSL https://example.com/health             # -f fails on HTTP error (no body output)
curl -o /dev/null -s -w "%{http_code}\n" https://example.com   # just the status code
```

## Killer flags

- `-L` — follow redirects
- `-i` / `-I` — include headers / HEAD-only
- `-s` / `-sS` — silent / silent but errors visible
- `-H` — header (repeatable)
- `-d` / `--data-binary` / `-F` — POST body (urlencoded / raw / multipart)
- `-o` / `-O` / `-OJ` — write body to file (explicit / from URL / from Content-Disposition)
- `-w` — custom timing/size/code output
- `-f` — fail on HTTP errors (exit non-zero, suppress body)
- `--resolve` / `--connect-to` — override DNS or routing
- `--max-time` / `--retry` — reliability knobs
- `--compressed` — Accept-Encoding + decompression
- `-k` — skip cert validation (testing only)
