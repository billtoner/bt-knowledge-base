# iwconfig

Configure and inspect wireless interfaces. Deprecated in favor of `iw` — and **doesn't speak WPA/WPA2/WPA3** (use `wpa_supplicant` or NetworkManager for those). Still useful for read-only inspection, channel/mode/power tweaks, and open or WEP networks.

**Tags:** wireless · network · deprecated

## Cool features

- **`iwconfig` with no args lists only *wireless* interfaces.** Skips ethernet/loopback — quick way to spot Wi-Fi NICs.
- **Mode switching is one command.** `iwconfig wlan0 mode monitor` for packet capture; `mode managed` for normal use.
- **Channel and tx-power are tunable inline.** Helpful when debugging signal or co-channel interference.
- **No WPA support.** Auth/encryption-wise it only knows open and WEP; for anything modern, `wpa_supplicant` does the actual association.
- **Deprecated; `iw` is the modern replacement.** Often missing on minimal systems.

## Inspect

```bash
iwconfig                          # all wireless interfaces
iwconfig wlan0                    # one interface — SSID, mode, freq, bit rate, signal
```

## Connect to an open network

```bash
sudo iwconfig wlan0 essid "CafeWiFi"
sudo iwconfig wlan0 essid "CafeWiFi" key off       # explicitly no encryption
```

## WEP (legacy)

```bash
sudo iwconfig wlan0 essid "OldNet" key s:password   # ASCII passphrase
sudo iwconfig wlan0 essid "OldNet" key 0123456789   # hex key
```

## Mode, channel, power

```bash
sudo iwconfig wlan0 mode managed                    # normal client
sudo iwconfig wlan0 mode monitor                    # packet capture
sudo iwconfig wlan0 mode ad-hoc                     # peer-to-peer
sudo iwconfig wlan0 channel 6                       # fix channel
sudo iwconfig wlan0 channel auto                    # let driver pick
sudo iwconfig wlan0 txpower 15                      # tx power in dBm
sudo iwconfig wlan0 power on                        # power saving on
sudo iwconfig wlan0 power off                       # power saving off (lower latency)
```

## Scanning (via iwlist)

```bash
sudo iwlist wlan0 scan                              # full scan dump
sudo iwlist wlan0 scan | grep -E "ESSID|Quality|Channel"
```

## Habit shifts — iwconfig → iw

| iwconfig / iwlist | iw |
|---|---|
| `iwconfig` | `iw dev` |
| `iwconfig wlan0` | `iw dev wlan0 info` + `iw dev wlan0 link` |
| `iwlist wlan0 scan` | `iw dev wlan0 scan` |
| `iwconfig wlan0 mode monitor` | `iw dev wlan0 set type monitor` |
| `iwconfig wlan0 channel 6` | `iw dev wlan0 set channel 6` |
| `iwconfig wlan0 txpower 15` | `iw dev wlan0 set txpower fixed 1500` (mBm) |

## Killer subcommands

- `essid <name>` — set SSID (or "any" to associate with anything available)
- `mode managed|monitor|ad-hoc|master` — interface role
- `channel <N|auto>` — set channel
- `txpower <dBm|auto|off>` — transmit power
- `power on|off` — power-saving toggle
- `rate <Mb|auto>` — bit rate (rarely needed)
