# httpie (`http` / `https`)

A user-friendly `curl` replacement. JSON-first, colorized output, sane defaults. Pairs naturally
with jq.

**Tags:** http · network · modern-unix

## Cool features

- **Auto-JSON by default.** Body is parsed and pretty-printed. Headers shown above the body in color.
- **Two commands** — `http` for HTTP, `https` for HTTPS. Otherwise identical.
- **POST/PUT/PATCH body via key=value.** Sends as JSON; no need to remember `-X POST -H "Content-Type:..."`.
- **Sessions** — `--session=name` persists cookies, headers, auth across calls.
- **Download mode.** `http --download URL` writes file with progress bar.
- **Form submissions.** `--form` flag toggles `application/x-www-form-urlencoded` mode.
- **Streaming uploads.** Pipe stdin into the body: `cat data.json | http POST host/api`.

## Syntax basics (way friendlier than curl)

```bash
# GET — just the URL
http GET https://api.github.com/users/billtoner

# Custom header
http GET host/api X-Auth-Token:my-token Accept:application/json

# POST JSON body (key=value pairs auto-marshal to JSON)
http POST host/api/users name=Bill role=admin
# becomes:  {"name": "Bill", "role": "admin"}

# POST with int / bool / array (use := for raw JSON values)
http POST host/api/users age:=42 admin:=true tags:='["dev","clinician"]'

# Auth (basic, digest, bearer)
http -a user:pass GET host/api
http -A bearer -a "ya29.token" GET host/api

# Follow redirects, verbose, no-color (for piping into jq)
http --follow --verbose GET host/api
http --print=b --headers=false GET host/api | jq '.foo'

# Save body to a file
http GET host/large-thing > /tmp/response.json
```

## Useful in FPOC

The Flask API on the Pi is the obvious target:

```bash
# Read current settings
http GET http://audiopulse-2:5001/api/settings | jq '.pressure_monitor'

# Start a session
http POST http://audiopulse-2:5001/api/session/start name=test_$(date +%s)

# Tweak threshold for one bucket (PATCH per-bucket write)
http PATCH http://audiopulse-2:5001/api/settings \
    category=pressure_monitor key=threshold side=left group=heel value:=120

# Stop the active session
http POST http://audiopulse-2:5001/api/session/stop

# Get a session debrief
http GET "http://audiopulse-2:5001/api/session/debrief?session_id=p001_walk_20260516_1400" \
    | jq '.score'

# Mac dashboard endpoints (running locally with AWS_PROFILE=audiopulse)
http GET http://localhost:5002/api/participants | jq '.[].id'
```

## Pairing with jq is the win

The default output is human-readable but if you pipe to jq, httpie strips colors automatically
and emits clean JSON. So the same command serves both eyes-on debugging AND scripted automation:

```bash
http GET host/api/sessions | jq '.[] | select(.duration > 60)'
http GET host/api/sessions | jq -r '.[].name' | xargs -I{} just debrief {}
```

## When NOT to use httpie

- **Scripts that need to handle errors precisely** — curl's exit codes are more granular.
  httpie exits 0 on most HTTP statuses by default (treat the response as data).
- **Performance-critical loops** — curl is lighter weight per invocation.
- **TLS edge cases** — curl has more knobs for client certs, custom CAs, etc.

For interactive API exploration, httpie wins every time. For production scripts, curl is the
old reliable.

## Useful flags

- `--print=hbHB` — pick which parts to show (request/response headers/body)
- `--verbose` / `-v` — full request + response trace
- `--follow` — follow 3xx redirects
- `--timeout 30` — request timeout in seconds
- `--check-status` — exit non-zero on 4xx/5xx (closer to curl behavior)
- `--session=NAME` — persist auth/headers across calls

## Install

```bash
brew install httpie    # already in Brewfile
```

## Companion: `xh`

A Rust-based reimplementation of httpie that starts faster (no Python interpreter spin-up). Same
syntax, basically a drop-in replacement. Install with `brew install xh` if startup time bothers
you. Not required.
