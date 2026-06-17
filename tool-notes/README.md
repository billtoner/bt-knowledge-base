# tool-notes

The notes themselves. One file per tool, with real-world examples.

This README is the **alphabetical view** — useful when you remember a
tool's name but not its category. For category browsing, start at
[`doc/bt-knowledge-base.md`](../doc/bt-knowledge-base.md) (categories) or one of
the [`doc/categories/`](../doc/categories/) files (tools per category).
For the style guide, see [`CLAUDE.md`](../CLAUDE.md).

## Tools

- [7z](7z.md) — high-ratio multi-format archiver with AES-256
- [aiomonitor](aiomonitor.md) — telnet console into a running asyncio loop
- [ansible](ansible.md) — configuration management and automation playbooks
- [apt](apt.md) — Debian/Ubuntu packages (apt + dpkg low-level queries)
- [atuin](atuin.md) — TUI fuzzy-search shell history backed by SQLite
- [awk](awk.md) — field/record text processing; the pattern-action workhorse
- [aws](aws.md) — AWS CLI v2; profiles, SSO, and every service API
- [az](az.md) — Azure CLI; auth, subscriptions, and Azure resources
- [bat](bat.md) — `cat` with syntax highlighting, line numbers, and git status
- [bluetoothctl](bluetoothctl.md) — interactive BlueZ Bluetooth control utility
- [bq](bq.md) — BigQuery CLI; query, load, extract, manage datasets
- [brew](brew.md) — Homebrew for macOS/Linux; formulae, casks, services
- [broot](broot.md) — interactive tree navigator; fuzzy search + actions
- [cron](cron.md) — scheduled jobs; crontab syntax + systemd-timer equivalents
- [curl](curl.md) — HTTP(S) client; headers, methods, multipart, debug tracing
- [db-browser-for-sqlite](db-browser-for-sqlite.md) — GUI for inspecting and editing SQLite databases
- [delta](delta.md) — syntax-highlighted, side-by-side git diff viewer
- [df](df.md) — filesystem free space (df) and per-directory usage (du)
- [direnv](direnv.md) — per-directory env vars, auto-loaded on cd
- [dmesg](dmesg.md) — kernel ring buffer; boot, hardware, OOM, driver messages
- [docker](docker.md) — build, run, and manage containers and images (+ compose)
- [doggo](doggo.md) — modern colorized dig; JSON, DoH/DoT, multi-resolver
- [eza](eza.md) — modern `ls` replacement with git status, icons, tree mode
- [fd](fd.md) — `find` replacement; smart-case, gitignore-aware, parallel exec
- [gcloud](gcloud.md) — Google Cloud CLI; auth, config, and GCP resources
- [gh](gh.md) — GitHub from the terminal; PRs, issues, releases, Actions, API
- [git](git.md) — version control fundamentals
- [gitleaks](gitleaks.md) — scan repos/files for committed secrets (this repo's hook)
- [glow](glow.md) — render markdown in the terminal (pairs with kb show)
- [go](go.md) — the Go toolchain; build, test, run, modules, vet
- [go-one-liners](go-one-liners.md) — quick Go from the shell; go run, docs, stdlib snippets
- [gpg](gpg.md) — encrypt, sign, verify; OpenPGP key management
- [gradle](gradle.md) — JVM builds (Gradle + Maven); tasks, deps, wrapper
- [graphviz](graphviz.md) — diagrams as code; render DOT graphs to SVG/PNG
- [grip](grip.md) — render local markdown via GitHub's API and serve on localhost
- [gron](gron.md) — flatten JSON into greppable assignments; reversible
- [gsutil](gsutil.md) — Google Cloud Storage from the CLI (gsutil + gcloud storage)
- [hcitool](hcitool.md) — lower-level Bluetooth utility (HCI commands, RSSI scans)
- [helm](helm.md) — Kubernetes package manager; install/template/rollback releases
- [htmlq](htmlq.md) — jq for HTML; extract with CSS selectors
- [htop](htop.md) — interactive process/resource monitor (htop; btop alt)
- [httpie](httpie.md) — friendly HTTP client; JSON by default, colorized output
- [ifconfig](ifconfig.md) — configure/inspect network interfaces (deprecated for `ip`)
- [iwconfig](iwconfig.md) — configure/inspect wireless interfaces (deprecated for `iw`)
- [jc](jc.md) — convert standard Unix command output to JSON for jq pipelines
- [journalctl](journalctl.md) — read and filter the systemd journal
- [jq](jq.md) — command-line JSON processor
- [just](just.md) — modern command runner; like make, but for tasks
- [kubectl](kubectl.md) — Kubernetes control-plane CLI: query and manage cluster resources
- [lazygit](lazygit.md) — full-screen TUI for git operations
- [lsblk](lsblk.md) — block devices, partitions, mounts, sizes as a tree
- [lscpu](lscpu.md) — CPU architecture, topology, caches, flags
- [lsof](lsof.md) — list open files: ports, sockets, locked mounts, deleted-but-open files
- [lspci](lspci.md) — list PCI devices; drivers, IDs, topology
- [lsusb](lsusb.md) — list USB devices and their topology
- [make](make.md) — the ubiquitous build/task runner; targets, prereqs, parallelism
- [ncdu](ncdu.md) — interactive 'what's eating my disk'; navigable du (dust alt)
- [nmcli](nmcli.md) — NetworkManager CLI; persistent profiles for Wi-Fi, Ethernet, VPN
- [nosql-workbench](nosql-workbench.md) — AWS GUI for DynamoDB schema design and querying
- [openssl](openssl.md) — TLS/crypto swiss army knife; certs, keys, CSRs, server debug
- [packer](packer.md) — build identical machine/container images from one config
- [pactl](pactl.md) — PulseAudio/PipeWire control utility
- [pandoc](pandoc.md) — universal document converter; markdown/HTML/PDF/docx and more
- [parted](parted.md) — partition disks (parted scriptable, fdisk interactive)
- [pass](pass.md) — Unix password store; gpg-encrypted files in a git repo
- [perf](perf.md) — CPU counters, sampling profiles, flame-graph output
- [pgrep](pgrep.md) — find and signal processes by name/attributes (pgrep, pkill)
- [pipx](pipx.md) — install Python CLI apps in isolated venvs
- [pre-commit](pre-commit.md) — manage/run git pre-commit hooks (ruff/pytest/secret scan)
- [procs](procs.md) — a modern ps; colored, tree, search, ports
- [psql](psql.md) — the PostgreSQL client; meta-commands, scripting, COPY, EXPLAIN
- [pulumi](pulumi.md) — IaC in real languages; stacks, config, encrypted secrets
- [py-spy](py-spy.md) — sampling profiler for running Python processes
- [qsv](qsv.md) — fast CSV toolkit; slice, stats, join, frequency, search
- [ripgrep](ripgrep.md) — `grep` replacement; recursive, smart-case, gitignore-aware
- [sar](sar.md) — historical + live system stats (sar; dstat for live)
- [scp](scp.md) — copy files over SSH; uses `~/.ssh/config` aliases
- [sed](sed.md) — stream editing; substitutions, ranges, in-place edits
- [sensors](sensors.md) — hardware temps, fans, voltages (lm-sensors)
- [sort](sort.md) — sort lines of text; numeric, by column, with deduplication
- [sqlite-utils](sqlite-utils.md) — CLI for SQLite queries, dumps, and JSON imports
- [sqlite3](sqlite3.md) — official SQLite CLI; schema, queries, pragmas
- [ssh](ssh.md) — secure shell; remote exec, port forwarding, jump hosts
- [ssh-add](ssh-add.md) — manage keys in the ssh-agent; macOS Keychain integration
- [ssh-keygen](ssh-keygen.md) — create/convert/inspect SSH keys; fingerprints, host keys
- [strace](strace.md) — trace syscalls and signals; first 'what is it doing' stop
- [systemctl](systemctl.md) — control systemd services and units
- [systemd-analyze](systemd-analyze.md) — boot timing and unit verification for systemd
- [tailscale](tailscale.md) — WireGuard mesh VPN; MagicDNS, ACLs, exit nodes
- [tar](tar.md) — create/extract archives; the flags you always re-look-up
- [terraform](terraform.md) — provision infrastructure as code; plan, apply, state, workspaces
- [terragrunt](terragrunt.md) — keep Terraform DRY across envs; remote state, module wiring
- [tig](tig.md) — TUI for browsing git log, diff, blame, and refs
- [tree](tree.md) — recursive directory listing as a tree
- [uv](uv.md) — fast Python project/dependency/env manager
- [vault](vault.md) — HashiCorp Vault; auth, KV secrets, dynamic creds, transit
- [vd](vd.md) — VisiData TUI spreadsheet; opens CSV/JSON/SQLite/Parquet
- [viztracer](viztracer.md) — trace-based async profiler with browser viewer
- [watch](watch.md) — re-run a command periodically; highlight changes
- [yq](yq.md) — YAML/TOML/JSON processor with jq-like syntax
- [zip](zip.md) — ZIP archives for cross-platform interop (zip/unzip)
- [zoxide](zoxide.md) — smarter `cd` based on frecency

- [zstd](zstd.md) — fast modern compression; great ratios, tunable levels
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
