# sensors

Read hardware temperatures, fan speeds, and voltages (lm-sensors).

## Use it

```bash
sensors                                # all detected sensors
sensors -f                             # report in Fahrenheit
sudo sensors-detect                    # one-time: probe + enable sensor modules
watch -n2 sensors                      # live monitoring (with the watch tool)
```

## Notes

- Run `sudo sensors-detect` once after install, then load the modules it suggests
- `sensors -j` emits JSON for dashboards; chip labels live in `/etc/sensors3.conf`
