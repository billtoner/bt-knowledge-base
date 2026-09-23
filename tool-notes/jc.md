# jc

Convert the output of common Unix commands to JSON. Lets you pipe `ps`, `df`, `dig`, `lsblk`, `systemctl`, `ifconfig`, `git log`, etc. straight into `jq`.

**Tags:** json · data

## Cool features

- **80+ parsers built in.** `jc --list-parsers` shows them all — covers most "annoying-to-parse" command output.
- **Two equivalent modes.** Magic form (`jc <cmd> <args>`) runs the command for you; pipe form (`<cmd> | jc --<parser>`) gives you full control of the source command.
- **`-p` pretty-prints** the JSON (default is compact).
- **Preserves exit codes** in magic mode — `jc -p curl -s api.example.com` propagates curl's exit.
- **Generic parsers too**: `--ini`, `--yaml`, `--xml`, `--csv`, `--kv` (key-value), `--semver`. Useful even when the command isn't well-known.

## Two ways to invoke

```bash
jc dig example.com                                # jc runs dig
dig example.com | jc --dig                         # same result via pipe
```

## Discoverability

```bash
jc --list-parsers                                  # all available
jc --help dig                                      # docs for one parser
```

## Real pipelines

```bash
# Processes
jc ps -ef | jq '.[] | select(.command | test("python")) | .pid'
jc -p ps aux | jq '.[] | select(.cpu_percent > 5)'

# Disk
jc df -h | jq '.[] | select((.use_percent|tonumber) > 80)'
jc lsblk | jq '.blockdevices[]'

# Network
jc ifconfig | jq '.[] | {name, ipv4_addr, mac_addr}'
jc netstat -an | jq '.[] | select(.state == "LISTEN")'
jc ss -tunlp | jq '.[]'
jc dig +short example.com | jq -r '.[].answer[]?.data'

# System
jc systemctl list-units | jq '.[] | select(.sub == "failed")'
jc -p uptime
jc -p uname -a
jc lsmod | jq '.[] | select(.size > 100000) | .module'
jc mount | jq '.[] | select(.filesystem_type == "nfs")'

# Files
jc ls -la | jq '.[] | select(.type == "f") | "\(.size) \(.filename)"'
jc -p stat /etc/passwd | jq '.[]'
jc find . -name '*.log' -mtime -1 | jq '.[]'

# Git
jc git log -n 20 | jq '.[] | {commit, author_name, date, message}'
```

## Generic parsers (when there's no command-specific parser)

```bash
cat ~/.aws/credentials | jc --ini | jq
cat docker-compose.yml | jc --yaml | jq '.services | keys'
cat data.csv | jc --csv | jq '.[]'
echo "1.2.3-rc.1" | jc --semver | jq
```

## Killer flags

- `-p` — pretty-print
- `-r` — raw output (don't parse, useful with `--meta-out`)
- `-q` — suppress parser warnings
- `--meta-out` — wrap output with metadata (parser used, timestamp, exit codes)
- `--list-parsers` — discover what's available
