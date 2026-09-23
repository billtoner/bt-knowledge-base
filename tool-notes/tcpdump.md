# tcpdump

Packet capture with BPF filters. The "I'll see for myself" tool when network behavior doesn't match what logs claim.

**Tags:** network · packets

## Cool features

- **BPF filters can match payload bytes.** Filter for "HTTP GET only" without capturing every TCP packet first.
- **`-G` rotates capture files by time.** Continuous capture without filling the disk.
- **`-w -` pipes raw pcap to stdout.** Capture remotely over SSH, analyze locally in Wireshark.

## Everyday captures

```bash
sudo tcpdump -i any -nn 'host 1.1.1.1'              # all traffic to/from a peer
sudo tcpdump -i any -nn -A 'tcp port 80'            # HTTP with ASCII payload
sudo tcpdump -i eth0 -nn -c 50 'port 53'            # 50 DNS packets, then stop
sudo tcpdump -i any -nn 'host 192.0.2.7 and not port 22'   # exclude your SSH session
```

## Save to pcap (and rotate)

```bash
sudo tcpdump -i any -nn -w out.pcap 'port 443'      # raw, full-fidelity capture
sudo tcpdump -i any -nn -w cap-%H%M.pcap -G 60      # new file every minute, time-stamped
```

## Filter on TCP flags

```bash
sudo tcpdump -i any -nn 'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0'
                                                    # connection setup + teardown only
sudo tcpdump -i any -nn 'tcp[tcpflags] = tcp-rst'   # resets — who's slamming connections shut?
```

## Match payload bytes (HTTP GET, TLS hello, etc.)

```bash
sudo tcpdump -i any -nn -A -s 0 \
  'tcp port 80 and (tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420)'
                                                    # 0x47 45 54 20 = "GET " — capture only HTTP GETs
```

## Remote capture, local Wireshark

```bash
ssh user@host "sudo tcpdump -i any -nn -w - 'port 53'" | wireshark -k -i -
                                                    # pipe live pcap into local Wireshark
```

## Killer flags

- `-i any` — every interface (Linux)
- `-nn` — no DNS, no port-to-service translation (faster, predictable output)
- `-A` — ASCII payload dump
- `-X` — hex + ASCII payload dump
- `-s 0` — full packet (older versions truncate by default)
- `-w FILE` — write pcap; `-` for stdout
- `-G N -w name-%H%M.pcap` — rotate every N seconds
- `-c N` — stop after N packets
