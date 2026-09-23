# iw

Modern wireless-interface command on Linux. Replaces `iwconfig` (which doesn't support WPA, monitor mode niceties, or modern radios).

**Tags:** wireless · network

## Cool features

- **`iw event`** streams every wireless event live — associate, disassociate, scan results, regulatory changes. Great for "what's actually happening when I lose wifi?"
- **`iw dev wlanX scan`** gives you signal strength and capabilities for every visible network, not just the SSID list `nmcli` shows.
- **`iw reg get`** tells you which regulatory domain is currently in effect — sometimes the reason a channel "doesn't exist."

## Current connection

```bash
iw dev wlan0 link                                 # BSSID, SSID, signal (dBm), bitrate, freq
iw dev wlan0 info                                 # mode, channel, txpower, type
```

## Scan for visible networks

```bash
sudo iw dev wlan0 scan | grep -E 'SSID|signal'    # quick view
sudo iw dev wlan0 scan | grep -A1 'SSID: ' | head -40
                                                  # peek at a chunk of results
```

## Connected stations (when you're the AP)

```bash
iw dev wlan0 station dump                         # signal, tx/rx rates, inactive time per client
```

## Regulatory domain

```bash
iw reg get                                        # which country code is in effect
sudo iw reg set US                                # set (locally — kernel may refuse for safety)
```

## Watch the radio live

```bash
iw event                                          # streams connect/disconnect/scan-done events
iw event -t                                       # with timestamps
```

## Monitor mode (capture raw 802.11)

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
                                                  # then capture with tcpdump / tshark on wlan0
```

## Killer commands

- `iw dev wlan0 link` — what am I connected to?
- `iw dev wlan0 scan` — what's around?
- `iw event` — live events
- `iw reg get` / `iw reg set` — regulatory domain
- `iw dev wlan0 set type monitor` — promiscuous wifi
