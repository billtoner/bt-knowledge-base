# cron

Scheduled jobs; crontab syntax and the systemd-timer equivalents.

## crontab

```bash
crontab -l                             # list your jobs
crontab -e                             # edit (installs on save)
crontab -l -u www-data                 # another user's jobs (as root)
```

## Schedule syntax (min hour dom mon dow)

- `0 3 * * *` — daily at 03:00
- `*/15 * * * *` — every 15 minutes
- `0 9 * * 1-5` — 09:00 on weekdays
- `@reboot` — once at boot

## systemd timers (the modern alternative)

```bash
systemctl list-timers --all            # next/last run of every timer
systemctl cat backup.timer             # see the schedule (OnCalendar=)
journalctl -u backup.service           # output from the last run
```

## Notes

- cron runs with a minimal PATH — use absolute paths or set PATH at the top
- systemd timers add logging, dependencies, and `Persistent=true` catch-up
