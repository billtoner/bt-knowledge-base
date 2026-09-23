# wg / wg-quick

WireGuard control plane. `wg` is the low-level command (status, runtime config); `wg-quick` is the friendly wrapper that reads `/etc/wireguard/<iface>.conf` and brings interfaces up/down.

**Tags:** vpn · network

## Cool features

- **`wg syncconf`** reloads the config without dropping existing connections. Routes/peers update; tunnels stay alive.
- **`wg show all dump`** is machine-parseable — one peer per line, tab-separated. Drop straight into a monitoring script.
- **The config file IS the source of truth.** `wg-quick up` just translates it to `wg` and `ip` commands you can run by hand if needed.

## Generate keys

```bash
umask 077                                         # so the private key isn't world-readable
wg genkey | tee privatekey | wg pubkey > publickey
wg genpsk > preshared                             # optional pre-shared key for added quantum-resistance
```

## Sample config

```ini
# /etc/wireguard/wg0.conf

[Interface]
Address    = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server-private-key>

[Peer]
PublicKey  = <peer-public-key>
AllowedIPs = 10.0.0.2/32                          # which IPs route through this peer
# Endpoint = peer.example.com:51820               # set on the client side; server discovers it
# PersistentKeepalive = 25                        # set on clients behind NAT
```

## Bring it up

```bash
sudo wg-quick up wg0                              # reads /etc/wireguard/wg0.conf
sudo wg-quick down wg0
sudo systemctl enable --now wg-quick@wg0          # auto-start on boot
```

## Status — what you'll look at 95% of the time

```bash
sudo wg show                                      # all interfaces, peers, endpoints, last handshake, tx/rx
sudo wg show wg0 latest-handshakes                # epoch timestamps per peer
sudo wg show wg0 transfer                         # bytes per peer
sudo wg show all dump                             # tab-separated, scriptable
```

## Add a peer at runtime (no restart)

```bash
sudo wg set wg0 peer <pubkey> \
    allowed-ips 10.0.0.5/32 \
    endpoint client.example.com:51820 \
    persistent-keepalive 25
```

## Reload config without dropping the tunnel

```bash
sudo wg syncconf wg0 <(wg-quick strip wg0)
                                                  # `strip` removes wg-quick-only directives (PostUp etc.)
                                                  # leaves only what `wg` itself understands
```

## Debugging "why is my tunnel quiet?"

```bash
sudo wg show wg0 latest-handshakes                # 0 means never; otherwise epoch of last handshake
                                                  # silence > ~3 minutes after a successful handshake = check NAT / keepalive
sudo ip route show table all | grep wg0           # is traffic being routed into the tunnel at all?
sudo tcpdump -i any -nn 'udp port 51820'          # are handshake packets even reaching you?
```

## Killer commands

- `wg show` / `wg show all dump`
- `wg-quick up/down <iface>`
- `wg set <iface> peer <pubkey> allowed-ips ...` — live peer changes
- `wg syncconf <iface> <(wg-quick strip <iface>)` — reload without tunnel drop
- `wg genkey | wg pubkey` — keypair in one pipe
