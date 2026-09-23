# bluetoothctl

Interactive and scripted control of BlueZ — Linux's Bluetooth stack. Pair devices, advertise discoverability, manage controllers.

**Tags:** hardware · bluetooth

## Cool features

- **Two modes.** Run with no args for an interactive `[bluetooth]#` REPL, or pass a command for one-shot use: `bluetoothctl power on`.
- **`discoverable-timeout 0` means no timeout.** Default is 180 seconds; set to 0 to stay discoverable indefinitely (useful when pairing a fiddly device).
- **`trust` separates from `pair`.** Trusted devices reconnect automatically; paired-but-untrusted devices require user confirmation each time.
- **Tab completion on MAC addresses** inside the REPL — type `connect ` and tab through known devices.
- **`scan on` runs until you say `scan off`.** It doesn't time out; remember to stop it or it keeps eating power.

## Make this machine discoverable

```bash
bluetoothctl power on                       # turn the controller on
bluetoothctl discoverable-timeout 0         # 0 = no timeout (default is 180s)
bluetoothctl discoverable on                # advertise to other devices
bluetoothctl pairable on                    # accept incoming pair requests
# ... later ...
bluetoothctl discoverable off               # stop advertising
```

## Pair a new device (e.g. headphones)

```bash
bluetoothctl                                # enter REPL
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on
# wait for device to appear, note its MAC address
[bluetooth]# pair AA:BB:CC:DD:EE:FF
[bluetooth]# trust AA:BB:CC:DD:EE:FF        # auto-reconnect in the future
[bluetooth]# connect AA:BB:CC:DD:EE:FF
[bluetooth]# scan off
[bluetooth]# quit
```

## Manage known devices

```bash
bluetoothctl devices                        # all known devices
bluetoothctl paired-devices                 # only paired
bluetoothctl info AA:BB:CC:DD:EE:FF         # detailed device info
bluetoothctl connect AA:BB:CC:DD:EE:FF
bluetoothctl disconnect AA:BB:CC:DD:EE:FF
bluetoothctl remove AA:BB:CC:DD:EE:FF       # forget the device entirely
```

## Controller inspection

```bash
bluetoothctl list                           # all controllers on this host
bluetoothctl show                           # default controller details
bluetoothctl select AA:BB:CC:DD:EE:FF       # switch active controller (multi-adapter setups)
```

## Killer commands

- `power on|off` — toggle the controller
- `discoverable on|off` — advertise to other devices
- `discoverable-timeout <secs>` — how long `discoverable on` lasts (0 = forever)
- `pairable on|off` — accept incoming pair requests
- `scan on|off` — actively search for nearby devices
- `pair <mac>` / `trust <mac>` / `connect <mac>` — the pairing trio
- `remove <mac>` — forget a device (undoes pair + trust)
