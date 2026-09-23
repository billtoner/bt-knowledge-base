# lsusb

List USB devices attached to the system. The quick "did the OS see my dongle?" check.

**Tags:** hardware · usb

## Cool features

- **`-t` shows a tree view** with hub topology, port numbers, device speeds (1.5M/12M/480M/5G). Handy for figuring out which hub a device is sitting behind.
- **`-d <vendor>:<product>`** filters by USB IDs — useful when writing udev rules and you need to confirm the exact IDs.
- **`-v` is *very* verbose** — descriptors, endpoints, supported configurations. Need `sudo` for some fields.
- **USB IDs are globally unique** — `<vendor>:<product>` like `046d:c52b`. Cross-reference at usb-ids.gowdy.us if a name comes through blank.

## Inspect

```bash
lsusb                             # all devices, one per line
lsusb -t                          # tree view (hubs, speeds, port numbers)
lsusb -v                          # verbose dump (long!)
sudo lsusb -v                     # some descriptors need root
```

## Filter

```bash
lsusb -d 046d:                    # all Logitech devices (vendor = 046d)
lsusb -d 046d:c52b                # specific Logitech unifying receiver
lsusb -s 001:003                  # by bus:device numbers (from default output)
lsusb -v -s 001:003               # verbose for one device only
```

## Common scenarios

```bash
# "Did the OS detect my USB stick?"
lsusb | grep -i kingston

# "What vendor:product do I need for a udev rule?"
lsusb -d 046d:                    # find the ID first, then write the rule

# "Is this device on USB 2 or USB 3?"
lsusb -t                          # tree view shows speeds (480M = 2.0, 5000M = 3.0)
```

## Killer flags

- `-t` — tree view with speeds and hub topology
- `-v` — verbose descriptors (combine with `-s`)
- `-d <vid>[:<pid>]` — filter by vendor/product ID
- `-s <bus>:<dev>` — filter by bus/device number
