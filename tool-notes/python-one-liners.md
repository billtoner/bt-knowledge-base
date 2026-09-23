# python-one-liners

`python3` tricks that earn their keep on the command line — no script file, no project, just one command.

**Tags:** scripting · one-liners · python

## Cool features

- **`-m` runs a stdlib module as a script.** `python3 -m http.server`, `python3 -m json.tool`, `python3 -m venv .venv`. Whole tools hiding in the stdlib.
- **`-c 'expr'`** lets you reach for any library function inline. Combined with `sys.stdin` it replaces most awk/sed-with-regex pain.
- **No deps to maintain.** Every modern Linux/macOS has it; nothing to install.

## Instant HTTP / file server

```bash
python3 -m http.server 8000                      # serve cwd on :8000
python3 -m http.server 8000 --directory /tmp     # serve a specific dir
python3 -m http.server --bind 127.0.0.1 8080     # localhost only
```

## JSON munging

```bash
curl -s https://api.example.com/x | python3 -m json.tool         # pretty-print
python3 -m json.tool < big.json | less                           # paged
python3 -c 'import json,sys; print(json.load(sys.stdin)["items"][0]["id"])' < data.json
                                                                  # extract a value
```

## Encode / decode

```bash
echo -n hello | python3 -c 'import base64,sys; print(base64.b64encode(sys.stdin.buffer.read()).decode())'
echo aGVsbG8= | python3 -c 'import base64,sys; sys.stdout.buffer.write(base64.b64decode(sys.stdin.read()))'
python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))' 'some string'
python3 -c 'import urllib.parse,sys; print(urllib.parse.unquote(sys.argv[1]))' 'some%20string'
```

## Random tokens & UUIDs

```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(32))'    # url-safe random token
python3 -c 'import secrets; print(secrets.token_hex(16))'        # hex
python3 -c 'import uuid; print(uuid.uuid4())'                    # UUID4
```

## Date math without dateutil

```bash
python3 -c 'import datetime as d; print((d.datetime.utcnow()+d.timedelta(days=30)).isoformat())'
python3 -c 'import time; print(int(time.time()))'                # unix epoch now
python3 -c 'import datetime as d; print(d.datetime.fromtimestamp(1700000000))'
                                                                 # epoch → human
```

## Quick benchmark

```bash
python3 -m timeit '[i*i for i in range(1000)]'                   # micro-bench an expression
python3 -m timeit -s 'import json; d={"x":1}' 'json.dumps(d)'    # with setup
```

## Throwaway venv

```bash
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install --user some-pkg                           # user-local install (no venv)
```

## Killer modules

- `-m http.server` — instant file server
- `-m json.tool` — pretty-print JSON
- `-m timeit` — micro-benchmark
- `-m venv` — virtualenv
- `-m pdb script.py` — debugger
- `-m this` — easter egg (`import this`)
