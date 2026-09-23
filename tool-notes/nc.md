# nc (`netcat`)

The TCP/UDP swiss army knife. Speak raw protocols, probe ports, glue stdio across the network, run a throwaway server in one line.

**Tags:** network

## Cool features

- **`-z` is "probe, don't connect."** Combined with `-v` it's the fastest way to ask "is this port open from where I am?"
- **`-l` flips it into server mode.** A few flags and you've got a one-shot file receiver or HTTP responder with no daemon to install.
- **Three netcats exist** (`nc.openbsd`, `nc.traditional`, `ncat`). The flags below assume the OpenBSD variant (default on macOS and most modern Linux). `ncat` (nmap) is a near-superset with TLS.

## Is this port reachable?

```bash
nc -zv example.com 443                            # one-shot reachability check
nc -zv example.com 22-443                         # probe a range (slow on big ranges — use nmap)
nc -zvw 2 example.com 443                         # 2-second timeout
```

## Banner / manual protocol

```bash
nc example.com 25                                 # SMTP greeting, then type HELO etc.
printf 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n' | nc example.com 80
                                                  # manual HTTP GET — see raw response
openssl s_client -connect example.com:443         # for TLS, swap nc for openssl s_client
```

## Throwaway listener / chat

```bash
nc -lvnp 4444                                     # listen on :4444 (TCP)
                                                  # second host: nc <listener-ip> 4444 to connect
```

## File transfer (no SSH needed on LAN)

```bash
# receiver:
nc -l 1234 > received.bin

# sender:
nc -q 1 receiver.local 1234 < file.bin            # -q 1 closes 1s after EOF
```

## Disposable one-shot HTTP responder

```bash
while true; do
    printf 'HTTP/1.1 200 OK\r\nContent-Length: 5\r\n\r\nhello' | nc -l -p 8080 -q 1
done
                                                  # answers every connection with "hello"
                                                  # useful for testing health-check pollers
```

## UDP

```bash
nc -u -l 12345                                    # UDP listener
echo ping | nc -u -w1 receiver.local 12345        # send one UDP datagram
```

## Killer flags

- `-z` — scan / probe; don't send data
- `-v` — verbose (says "succeeded" / "refused")
- `-l` — listen
- `-n` — no DNS lookups
- `-p PORT` — bind to a specific local port (listener)
- `-u` — UDP
- `-w SEC` — connect timeout
- `-q SEC` — quit SEC after EOF on stdin
