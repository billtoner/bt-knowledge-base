# hcitool

Low-level Bluetooth control via raw HCI commands. **Deprecated** in BlueZ 5; many subcommands have been removed on newer distros. Most use cases now belong to `bluetoothctl` or `btmgmt`, but `hcitool` is still useful when scripting RSSI checks or talking to legacy stacks.

**Tags:** hardware · bluetooth · deprecated

## Cool features

- **`lescan`** — pre-`bluetoothctl` way to discover BLE devices, still works on systems where it's installed.
- **`rssi`** reports signal strength of an active connection — handy for proximity scripts.
- **`inq`** (inquiry) includes RSSI and device class along with addresses — more data than plain `scan`.
- **Deprecation reality check.** Many subcommands now print "Command not supported" on modern BlueZ. `bluetoothctl` and `btmgmt` are the replacements.

## Adapters

```bash
hcitool dev                       # list local Bluetooth adapters
```

## Discover devices

```bash
sudo hcitool scan                 # classic BT inquiry (names + addresses)
sudo hcitool inq                  # inquiry with class + RSSI
sudo hcitool lescan               # BLE scan (Ctrl-C to stop)
sudo hcitool lescan --duplicates  # don't deduplicate — useful for beacon work
```

## Query a remote device

```bash
hcitool name AA:BB:CC:DD:EE:FF    # get device name
hcitool info AA:BB:CC:DD:EE:FF    # features, version, manufacturer
```

## Connections

```bash
hcitool con                       # list active connections (classic + LE)
sudo hcitool cc AA:BB:CC:DD:EE:FF # create classic connection
sudo hcitool dc AA:BB:CC:DD:EE:FF # disconnect
hcitool rssi AA:BB:CC:DD:EE:FF    # RSSI for an active connection (must be connected)
```

## Habit shifts — hcitool → bluetoothctl / btmgmt

| hcitool | modern equivalent |
|---|---|
| `hcitool dev` | `bluetoothctl list` |
| `hcitool scan` | `bluetoothctl scan on` |
| `hcitool lescan` | `bluetoothctl scan on` (with LE controller) or `btmgmt find` |
| `hcitool inq` | `btmgmt find` |
| `hcitool con` | `bluetoothctl devices Connected` |
| `hcitool info <mac>` | `bluetoothctl info <mac>` |
| `hcitool name <mac>` | `bluetoothctl info <mac>` and grep `Name` |

## Killer subcommands

- `dev` — list adapters
- `scan` / `inq` — classic discovery (inq adds class + RSSI)
- `lescan` — BLE discovery
- `con` — active connections
- `rssi <mac>` — signal strength of a connected peer
- `info <mac>` — features/version/manufacturer of a remote device
