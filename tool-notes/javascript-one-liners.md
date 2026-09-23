# javascript-one-liners

`node -e '...'` and `npx <tool>` tricks. JavaScript on the command line without a project or `npm init`.

**Tags:** scripting · one-liners · javascript

## Cool features

- **`node -e 'expr'`** runs any expression; full stdlib (`fs`, `crypto`, `http`, `url`, `path`) is available.
- **`npx <tool>`** runs a one-off package without installing globally. `http-server`, `serve`, `kill-port`, `prettier` just work.
- **`Buffer`** is the universal encode/decode for base64 and hex — no library needed.

## Instant HTTP / file server

```bash
npx http-server -p 8000                          # serve cwd; no install
npx serve -p 8000                                # alternative
node -e "require('http').createServer((q,r)=>{r.end('ok')}).listen(8080)"
                                                 # one-liner hello-world server on :8080
```

## Encode / decode

```bash
node -e "console.log(Buffer.from('hello').toString('base64'))"               # base64 encode
node -e "console.log(Buffer.from('aGVsbG8=','base64').toString())"           # base64 decode
node -e "console.log(Buffer.from('hello').toString('hex'))"                  # hex encode
node -e "console.log(encodeURIComponent(process.argv[1]))" 'some string'     # URL encode
node -e "console.log(decodeURIComponent(process.argv[1]))" 'some%20string'   # URL decode
```

## JSON munging from stdin

```bash
curl -s https://api.example.com/x | \
    node -e 'let d=""; process.stdin.on("data",c=>d+=c).on("end",()=>console.log(JSON.parse(d).items[0].id))'
```

## Random tokens / UUIDs

```bash
node -e "console.log(crypto.randomUUID())"                                   # UUID4 (Node 14.17+)
node -e "console.log(crypto.randomBytes(32).toString('hex'))"                # 64-hex token
node -e "console.log(crypto.randomBytes(24).toString('base64url'))"          # url-safe token
```

## Date math

```bash
node -e "console.log(new Date(Date.now()+30*86400e3).toISOString())"         # 30 days from now
node -e "console.log(Math.floor(Date.now()/1000))"                           # unix epoch now
node -e "console.log(new Date(1700000000*1000).toISOString())"               # epoch → ISO
```

## Useful npx tools

```bash
npx kill-port 3000                                                           # free whatever's on :3000
npx prettier --write 'src/**/*.js'                                           # format
npx json-server db.json                                                      # quick REST mock from JSON
npx tldr <cmd>                                                               # community man pages
```

## Killer flags

- `-e 'expr'` — run a single expression
- `-p 'expr'` — like `-e` but auto-prints the result
- `--inspect-brk script.js` — start with debugger paused at line 1
- `--watch script.js` — auto-rerun on file changes (Node 18.11+)
