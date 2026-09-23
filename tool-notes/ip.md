# ip (`iproute2`)

The modern replacement for `ifconfig`, `route`, and `arp`. One command for everything to do with interfaces, addresses, routes, and neighbors.

**Tags:** network

## Cool features

- **`ip route get`** tells you exactly which interface, gateway, and source IP the kernel would use for a destination. Beats squinting at the routing table.
- **`-br -c`** gives brief, colored output — instant readable summary of a multi-interface host.
- **`-j` emits JSON.** Real scripting instead of awk-on-whitespace.

## Quick scan of the host

```bash
ip -br -c addr                          # one line per interface, colored
ip -br link                             # link state only (UP/DOWN, MAC)
ip -s link show eth0                    # rx/tx packet, byte, drop, error counters
```

## "Which interface will be used for this destination?"

```bash
ip route get 8.8.8.8                    # interface, gateway, src IP picked for this destination
ip route get 10.0.5.7 from 192.168.1.5  # simulate from a specific source address
```

## Routing table edits

```bash
sudo ip route add 10.0.0.0/8 via 192.168.1.1
sudo ip route add default via 192.168.1.1 dev eth0
sudo ip route del 10.0.0.0/8
ip route show table all                 # every table — local / main / default
```

## ARP / neighbor table

```bash
ip neigh                                # current ARP cache (replaces `arp -a`)
sudo ip neigh flush dev eth0            # drop the table — forces fresh ARPs
```

## Network namespaces

```bash
sudo ip netns add testns                # fresh namespace
sudo ip netns exec testns bash          # shell inside it (loopback only by default)
sudo ip netns list
```

## Watch state changes live

```bash
ip monitor link addr route              # live events: link up/down, addr changes, route adds
```

## JSON for scripts

```bash
ip -j addr | jq '.[] | {ifname, addr: [.addr_info[].local]}'
                                        # ifname + every assigned IP, no awk
```

## Habit shifts from ifconfig / route / arp

| Old | New |
|---|---|
| `ifconfig -a` | `ip -br addr` |
| `ifconfig eth0 up` | `ip link set eth0 up` |
| `route -n` | `ip route` |
| `arp -a` | `ip neigh` |
| `route add default gw …` | `ip route add default via …` |
| `ifconfig eth0 mtu 1450` | `ip link set eth0 mtu 1450` |
