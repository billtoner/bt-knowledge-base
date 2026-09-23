# watch

Re-run a command at a fixed interval, showing each run's output in place. Default interval is 2 seconds.

> macOS doesn't ship `watch` — install with `brew install watch`.

**Tags:** monitoring · shell

## Cool features

- **`-d` highlights what changed** since the previous run — instant visual diff.
- **`-d=cumulative`** keeps the highlight on any cell that has *ever* changed in this watch session. Great for spotting intermittent values.
- **`-c` preserves ANSI colors** from commands like `git status`, `ls --color`, `kubectl get` — otherwise you get a wash of plain text.
- **`-g` exits when output changes** — `watch -g` is a "wait until this changes" primitive for scripts.
- **`-n <secs>` supports sub-second intervals** — `watch -n 0.5 free -h` ticks twice per second.
- **`-x`** passes the command via `exec` (no shell). Useful when complex quoting in the argv would otherwise confuse `watch`.

## Basic

```bash
watch ps aux                         # default 2s interval
watch -n 1 ps aux                    # 1s
watch -n 0.5 free -h                 # 500ms
watch -n 5 'df -h | grep /dev'       # quote when the command has shell features
```

## Highlight what changed

```bash
watch -d free -h                     # highlight changed cells each tick
watch -d=cumulative free -h          # highlight stays once anything has changed
```

## Preserve colors

```bash
watch -c -d 'git status'
watch -c -d 'ls --color=always -la'
watch -c -d 'kubectl get pods -A'
```

## Wait until output changes, then exit

```bash
watch -g 'ls /tmp/flag'              # exits as soon as output differs (e.g. file appears)
watch -g 'curl -s -o /dev/null -w "%{http_code}" http://service/health'
```

## No header, more screen space

```bash
watch -t -n 1 free -h                # no top header
```

## Common one-liners

```bash
watch -d -n 1 'docker ps'
watch -d -n 2 'kubectl get pods -A'
watch -d -n 1 'df -h | grep -v tmpfs'
watch -d -n 5 'find . -name "*.log" -mmin -1 -ls'    # files modified in last minute
watch -c -d -n 2 'git -c color.status=always status'
watch -d -n 1 'systemctl --failed'                   # any units fall over?
watch -d -n 2 'nmcli device wifi list'               # Wi-Fi signal drifting
watch -d -n 5 'curl -s https://api.example.com/health | jq .'
```

## Killer flags

- `-n <secs>` — interval (supports decimals)
- `-d [=cumulative]` — highlight differences (cumulative keeps history)
- `-c` — interpret ANSI color codes
- `-g` — exit on first change (one-shot wait-for-change)
- `-t` — suppress header
- `-x` — exec without shell (cleaner argv handling)
- `-b` — beep on non-zero exit
- `-e` — exit on non-zero exit
