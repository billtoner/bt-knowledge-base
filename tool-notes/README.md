# tool-notes

The notes themselves. One file per tool, with real-world examples.

This README is the **alphabetical view** — useful when you remember a
tool's name but not its category. For category browsing, start at
[`doc/bt-knowledge-base.md`](../doc/bt-knowledge-base.md) (categories) or one of
the [`doc/categories/`](../doc/categories/) files (tools per category).
For the style guide, see [`CLAUDE.md`](../CLAUDE.md).

## Tools

- [aiomonitor](aiomonitor.md) — telnet console into a running asyncio loop
- [ansible](ansible.md) — configuration management and automation playbooks
- [atuin](atuin.md) — TUI fuzzy-search shell history backed by SQLite
- [bat](bat.md) — `cat` with syntax highlighting, line numbers, and git status
- [bluetoothctl](bluetoothctl.md) — interactive BlueZ Bluetooth control utility
- [curl](curl.md) — HTTP(S) client; headers, methods, multipart, debug tracing
- [db-browser-for-sqlite](db-browser-for-sqlite.md) — GUI for inspecting and editing SQLite databases
- [delta](delta.md) — syntax-highlighted, side-by-side git diff viewer
- [eza](eza.md) — modern `ls` replacement with git status, icons, tree mode
- [fd](fd.md) — `find` replacement; smart-case, gitignore-aware, parallel exec
- [git](git.md) — version control fundamentals
- [grip](grip.md) — render local markdown via GitHub's API and serve on localhost
- [gron](gron.md) — flatten JSON into greppable assignments; reversible
- [hcitool](hcitool.md) — lower-level Bluetooth utility (HCI commands, RSSI scans)
- [httpie](httpie.md) — friendly HTTP client; JSON by default, colorized output
- [ifconfig](ifconfig.md) — configure/inspect network interfaces (deprecated for `ip`)
- [iwconfig](iwconfig.md) — configure/inspect wireless interfaces (deprecated for `iw`)
- [jc](jc.md) — convert standard Unix command output to JSON for jq pipelines
- [journalctl](journalctl.md) — read and filter the systemd journal
- [jq](jq.md) — command-line JSON processor
- [lazygit](lazygit.md) — full-screen TUI for git operations
- [lsusb](lsusb.md) — list USB devices and their topology
- [nmcli](nmcli.md) — NetworkManager CLI; persistent profiles for Wi-Fi, Ethernet, VPN
- [nosql-workbench](nosql-workbench.md) — AWS GUI for DynamoDB schema design and querying
- [pactl](pactl.md) — PulseAudio/PipeWire control utility
- [py-spy](py-spy.md) — sampling profiler for running Python processes
- [ripgrep](ripgrep.md) — `grep` replacement; recursive, smart-case, gitignore-aware
- [scp](scp.md) — copy files over SSH; uses `~/.ssh/config` aliases
- [sort](sort.md) — sort lines of text; numeric, by column, with deduplication
- [sqlite-utils](sqlite-utils.md) — CLI for SQLite queries, dumps, and JSON imports
- [sqlite3](sqlite3.md) — official SQLite CLI; schema, queries, pragmas
- [ssh](ssh.md) — secure shell; remote exec, port forwarding, jump hosts
- [ssh-add](ssh-add.md) — manage keys in the ssh-agent; macOS Keychain integration
- [systemctl](systemctl.md) — control systemd services and units
- [tig](tig.md) — TUI for browsing git log, diff, blame, and refs
- [vd](vd.md) — VisiData TUI spreadsheet; opens CSV/JSON/SQLite/Parquet
- [viztracer](viztracer.md) — trace-based async profiler with browser viewer
- [watch](watch.md) — re-run a command periodically; highlight changes
- [yq](yq.md) — YAML/TOML/JSON processor with jq-like syntax
- [zoxide](zoxide.md) — smarter `cd` based on frecency

## Quick search recipes

From this directory:

```bash
# Find a tool note by name fragment
fd <fragment> -e md

# Find tools whose notes mention a keyword
rg -li <keyword> .

# Fuzzy-pick and preview (needs fzf + bat)
fd . -e md | fzf --preview 'bat --color=always {}'

# List every tool currently documented
fd . -e md -x basename {} .md | sort
```

## Adding a new tool

See [`../CLAUDE.md`](../CLAUDE.md). In short:

1. Write `<tool>.md` here in the style of [ripgrep.md](ripgrep.md).
2. Add a bullet to the appropriate `doc/categories/<cat>.md`.
3. Add a bullet to this README (alphabetical position).
4. If creating a new category, convert its placeholder in
   `doc/bt-knowledge-base.md` to a link.
