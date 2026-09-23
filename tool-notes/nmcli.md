# nmcli

Command-line interface to NetworkManager. Manages Wi-Fi, Ethernet, VPN, mobile broadband, and bridge/bond/team connections as **persistent profiles** — settings survive reboot, unlike raw `ip` commands.

**Tags:** network · wireless

## Cool features

- **Persistent profiles.** Every connection is a saved profile under `/etc/NetworkManager/system-connections/` — reconnect on boot, no scripts needed.
- **Abbreviations work everywhere.** `nmcli c s` == `nmcli connection show`; `nmcli d w l` == `nmcli device wifi list`.
- **Tab completion knows your connections.** Typing `nmcli c up <TAB>` lists saved profile names.
- **`+prop` and `-prop` on list values.** `+ipv4.dns 9.9.9.9` appends; `-ipv4.dns 8.8.8.8` removes. No need to rewrite the whole list.
- **`--ask`** prompts interactively for any missing secrets — useful when you don't want passwords in shell history.
- **`-t` is the scriptable form.** Colon-separated, no headers. Combine with `-f <fields>` to pick columns.
- **Speaks WPA/WPA2/WPA3** — unlike `iwconfig`, which is open/WEP only.
- **`nmcli monitor`** streams events live (device state, connection up/down, IP changes).

## Status & inspection

```bash
nmcli                                  # overall status — devices + connections
nmcli general status                   # one-line summary
nmcli device status                    # interface table: name, type, state, connection
nmcli connection show                  # all saved profiles
nmcli connection show --active         # only currently-active profiles
nmcli connection show "MyWiFi"         # all properties of one profile
nmcli device show wlan0                # device details (IP, DNS, MAC, speed)
```

## Wi-Fi: scan and connect

```bash
nmcli device wifi list                 # nearby networks with signal/security
nmcli device wifi rescan               # force a fresh scan
nmcli device wifi connect "MyWiFi" password "secret"
nmcli device wifi connect "MyWiFi" password "secret" hidden yes
nmcli device wifi connect "MyWiFi" password "secret" --ask  # other secrets prompted
```

## Radio (Wi-Fi / WWAN / airplane mode)

```bash
nmcli radio wifi                       # show state
nmcli radio wifi off                   # turn Wi-Fi off
nmcli radio wifi on
nmcli radio all off                    # airplane mode
```

## Up / down / delete saved connections

```bash
nmcli connection up   "MyWiFi"
nmcli connection down "MyWiFi"
nmcli connection delete "MyWiFi"
nmcli connection reload                # re-read from disk after manual edits
```

## Static IP (modify a profile)

```bash
nmcli connection modify "MyWiFi" \
    ipv4.method manual \
    ipv4.addresses 192.168.1.50/24 \
    ipv4.gateway 192.168.1.1 \
    ipv4.dns "1.1.1.1 9.9.9.9"
nmcli connection up "MyWiFi"           # apply
nmcli connection modify "MyWiFi" ipv4.method auto      # back to DHCP
```

## DNS tweaks without rewriting the list

```bash
nmcli connection modify "MyWiFi" +ipv4.dns "8.8.8.8"   # append
nmcli connection modify "MyWiFi" -ipv4.dns "8.8.8.8"   # remove
nmcli connection modify "MyWiFi" ipv4.ignore-auto-dns yes   # ignore DHCP-provided DNS
```

## Create a new connection from scratch

```bash
# Static ethernet
nmcli connection add type ethernet con-name "wired-static" ifname eth0 \
    ip4 192.168.1.50/24 gw4 192.168.1.1

# DHCP ethernet
nmcli connection add type ethernet con-name "wired-dhcp" ifname eth0

# Bridge
nmcli connection add type bridge con-name br0 ifname br0
nmcli connection add type ethernet con-name br0-port1 ifname eth0 master br0
```

## Wi-Fi hotspot

```bash
nmcli device wifi hotspot ssid "MyHotspot" password "supersecret"
nmcli device wifi hotspot ifname wlan0 ssid "Guest" password "letmein" band bg
nmcli connection down Hotspot          # stop sharing
```

## VPN

```bash
nmcli connection import type openvpn file ./client.ovpn
nmcli connection up client --ask                       # prompt for creds
nmcli connection import type wireguard file ./wg0.conf
```

## Scriptable output

```bash
nmcli -t -f NAME,UUID,TYPE connection show              # terse, colon-separated
nmcli -t -f ACTIVE,SSID device wifi list | grep '^yes'  # current SSID
nmcli -g GENERAL.STATE device show wlan0                # one field, no labels
```

## Watch events live

```bash
nmcli monitor                          # all NetworkManager events
nmcli device monitor                   # device state changes only
```

## Habit shifts — nmcli vs alternatives

| Goal | nmcli | Alternative |
|---|---|---|
| Connect to WPA Wi-Fi | `nmcli d w connect SSID password ...` | `wpa_supplicant` + config file |
| Persistent static IP | `nmcli c modify ... ipv4.method manual ...` | `/etc/network/interfaces` (Debian-ish), `netplan` (Ubuntu) |
| Temporary IP change | `nmcli c modify` + `c up` | `ip addr add` (vanishes on reboot) |
| Scan Wi-Fi | `nmcli d w list` | `iw dev wlan0 scan`, `iwlist wlan0 scan` |

## Killer flags / patterns

- `-t` — terse (colon-separated, no headers) — for scripts
- `-f <fields>` — pick columns (e.g. `-f NAME,STATE,DEVICE`)
- `-g <field>` — single field, raw value (great for `$(...)`)
- `-p` — pretty (aligned, sectioned)
- `-c yes` — force colorized output (even when piped)
- `+prop` / `-prop` — append/remove on list properties (dns, addresses, routes)
- `--ask` — prompt for any missing secrets
- Abbreviations: `c` (connection), `d` (device), `g` (general), `r` (radio), `n` (networking), `m` (monitor)
