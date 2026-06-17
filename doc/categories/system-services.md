# System & Services

Inspecting and controlling the running system — systemd units, the journal, and the files and ports processes hold open.

- [systemctl](../../tool-notes/systemctl.md) — control units, query state, edit configs safely
- [journalctl](../../tool-notes/journalctl.md) — query the systemd journal with filters for unit, time, boot, and priority
- [lsof](../../tool-notes/lsof.md) — what files, sockets, and ports a process holds open
- [cron](../../tool-notes/cron.md) — scheduled jobs; crontab syntax + systemd-timer equivalents
- [pgrep](../../tool-notes/pgrep.md) — find and signal processes by name/attributes (pgrep, pkill)
- [dmesg](../../tool-notes/dmesg.md) — kernel ring buffer; boot, hardware, OOM, driver messages
- [systemd-analyze](../../tool-notes/systemd-analyze.md) — boot timing and unit verification for systemd
