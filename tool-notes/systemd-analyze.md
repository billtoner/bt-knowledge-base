# systemd-analyze

Boot performance and unit verification for systemd.

## Boot timing

```bash
systemd-analyze                        # total boot time, split by phase
systemd-analyze blame                  # slowest units, worst first
systemd-analyze critical-chain         # the dependency chain that gated boot
systemd-analyze plot > boot.svg        # render the boot timeline as SVG
```

## Validate & inspect

```bash
systemd-analyze verify my.service      # lint a unit file
systemd-analyze cat-config systemd/system.conf   # merged config + drop-ins
systemd-analyze security sshd.service  # sandboxing/exposure score for a unit
```

## Notes

- `security` is a great hardening checklist — it scores each unit's isolation
- `plot` writes to stdout; redirect to a file and open it in a browser
