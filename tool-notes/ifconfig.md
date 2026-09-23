# ifconfig

Configure and inspect network interfaces. Deprecated in favor of `ip` (iproute2), but still installed on many systems and faster to recall when you need a quick look.

**Tags:** network · deprecated

## Cool features

- **`ifconfig` with no args lists all *up* interfaces.** Use `-a` to include downed ones.
- **MAC address spoofing.** `ifconfig eth0 hw ether AA:BB:CC:DD:EE:FF` after taking the interface down — useful for captive portals or testing.
- **IP aliases with `eth0:0` syntax.** Add a second address on the same NIC without virtual interface gymnastics.
- **MTU tweaking inline.** `ifconfig eth0 mtu 1400` — handy when chasing PMTU / VPN fragmentation issues.
- **Deprecated but ubiquitous.** Often missing on minimal systems (Alpine, recent Debian/Ubuntu installs). `ip` is the modern replacement.

## Inspect

```bash
ifconfig                          # all up interfaces
ifconfig -a                       # include downed interfaces
ifconfig eth0                     # just one interface
ifconfig -s                       # short table: name, MTU, RX/TX counts, errors
```

## Bring up / down

```bash
sudo ifconfig eth0 up
sudo ifconfig eth0 down
```

## Assign / change IP

```bash
sudo ifconfig eth0 192.168.1.10 netmask 255.255.255.0
sudo ifconfig eth0 192.168.1.10 netmask 255.255.255.0 broadcast 192.168.1.255
sudo ifconfig eth0:0 192.168.1.11                   # alias — second IP on same NIC
sudo ifconfig eth0:0 down                           # remove the alias
```

## MAC and MTU

```bash
sudo ifconfig eth0 down
sudo ifconfig eth0 hw ether AA:BB:CC:DD:EE:FF       # change MAC
sudo ifconfig eth0 up
sudo ifconfig eth0 mtu 1400                          # change MTU
```

## Habit shifts — ifconfig → ip

| ifconfig | ip |
|---|---|
| `ifconfig` | `ip addr` (or `ip a`) |
| `ifconfig -a` | `ip -br addr` (brief, one line per iface) |
| `ifconfig eth0 up` | `ip link set eth0 up` |
| `ifconfig eth0 192.168.1.10 netmask 255.255.255.0` | `ip addr add 192.168.1.10/24 dev eth0` |
| `ifconfig eth0 hw ether AA:BB:...` | `ip link set eth0 address AA:BB:...` |
| `route -n` | `ip route` |

## Killer flags

- `-a` — include downed interfaces
- `-s` — short summary table (counters)
- `up` / `down` — toggle interface state
- `hw ether <MAC>` — change hardware address
- `mtu <N>` — change MTU
