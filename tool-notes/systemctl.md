# systemctl

Front door to systemd. Start/stop/enable services, inspect state, and edit units safely.

**Tags:** systemd · services

## Cool features

- **`--now` combo flag.** `enable --now` and `disable --now` do both states in one command — no need to enable *and* start as separate steps.
- **Drop-in overrides survive package upgrades.** `systemctl edit foo` writes to `/etc/systemd/system/foo.service.d/override.conf` — the package's unit file stays untouched.
- **Scriptable status checks.** `is-active` and `is-enabled` print one word and set exit codes — easy to use in shell guards.
- **`systemctl cat`** shows the active unit file plus all drop-ins merged, so you see exactly what systemd sees.
- **`systemd-run`** spins up a transient service with full systemd controls (resource limits, calendar timers) for one-off jobs.
- **Boot analysis built in.** `systemd-analyze blame` ranks slow units; `systemd-analyze plot > boot.svg` renders an SVG timeline of the whole boot.

## Lifecycle

```bash
sudo systemctl start  nginx
sudo systemctl stop   nginx
sudo systemctl restart nginx
sudo systemctl reload nginx                 # SIGHUP — re-read config without dropping connections
sudo systemctl enable --now nginx           # start now AND on boot
sudo systemctl disable --now nginx          # stop now AND remove from boot
```

## Status & inspection

```bash
systemctl status nginx                      # state, recent logs, PID, cgroup tree
systemctl is-active nginx                   # scriptable: "active" / "inactive"
systemctl is-enabled nginx                  # scriptable: "enabled" / "disabled" / "masked"
systemctl cat nginx                         # unit file + drop-ins as systemd sees it
systemctl show nginx                        # every property, key=value
systemctl show nginx -p MainPID,ActiveState,SubState
```

## What's running / what's broken

```bash
systemctl list-units --type=service                  # active services
systemctl list-units --type=service --state=failed   # only failures
systemctl --failed                                   # shortcut
systemctl list-unit-files --state=enabled            # everything that starts at boot
systemctl list-dependencies nginx                    # dependency tree
```

## Editing units safely

```bash
sudo systemctl edit nginx                   # drop-in override — survives package upgrades
sudo systemctl edit --full nginx            # edit the whole unit file
sudo systemctl daemon-reload                # after hand-editing unit files
```

## Boot analysis

```bash
systemd-analyze                             # total boot time
systemd-analyze blame                       # slowest units, ranked
systemd-analyze critical-chain              # what's on the critical path
systemd-analyze plot > boot.svg             # SVG timeline of boot
```

## Transient services

```bash
systemd-run --unit=backup --on-calendar='daily' /usr/local/bin/backup.sh
systemd-run --scope -p MemoryMax=512M ./hungry-script.py
```

## Killer flags

- `--now` — combine `enable`/`disable` with `start`/`stop`
- `--user` — operate on the user-level systemd instance (no sudo)
- `--state=failed` — narrow `list-units` to broken ones only
- `-p <prop>` — with `show`, print only specific properties
