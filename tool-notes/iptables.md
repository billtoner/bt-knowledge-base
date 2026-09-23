# iptables

The venerable Linux packet filter. Rules live in **chains** (`INPUT`, `OUTPUT`, `FORWARD`) and **tables** (filter, nat, mangle). Order matters — first match wins per chain.

Note: most modern distros run `iptables-nft` under the hood — the CLI here translates to nftables rules. Coexisting `nft` and `iptables` commands can confuse each other; pick one for any given host.

**Tags:** firewall · network

## Cool features

- **`-m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT`** is the one rule that makes a sane stateful firewall possible. Almost every ruleset starts with it.
- **`-m recent`** gives you per-source rate limiting without a separate daemon.
- **`-I CHAIN N`** inserts at position N — useful when you need a rule to win against an already-loaded set without reorganizing.

## See what's loaded

```bash
sudo iptables -L -v -n --line-numbers             # all filter chains with counters + line nos
sudo iptables -t nat -L -v -n                     # NAT table
sudo iptables -S                                  # rules as restorable commands
```

## A sane baseline

```bash
sudo iptables -P INPUT DROP                       # default deny inbound
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

sudo iptables -A INPUT -i lo -j ACCEPT                                       # loopback
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT  # stateful
sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT            # let pings in
sudo iptables -A INPUT -p tcp -m multiport --dports 22,80,443 -j ACCEPT      # services
```

## Restrict by source

```bash
sudo iptables -A INPUT -p tcp --dport 22 -s 10.0.0.0/8 -j ACCEPT
sudo iptables -I INPUT 1 -s 192.0.2.7 -j DROP     # bad actor blackhole at top
```

## NAT — port redirect and outbound masquerade

```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
                                                  # rewrite incoming 80 → local 8080

sudo iptables -t nat -A PREROUTING -p tcp --dport 443 \
    -j DNAT --to-destination 10.0.0.5:443         # forward 443 to internal host
sudo iptables -t nat -A POSTROUTING -j MASQUERADE # NAT outbound replies
```

## Rate limiting (built-in, no fail2ban)

```bash
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW \
    -m recent --set
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW \
    -m recent --update --seconds 60 --hitcount 4 -j DROP
                                                  # >3 new SSH connections / minute from one IP → drop
```

## Persist

```bash
# Debian/Ubuntu with iptables-persistent:
sudo iptables-save > /etc/iptables/rules.v4

# Generic save/restore:
sudo iptables-save  > /etc/iptables.rules
sudo iptables-restore < /etc/iptables.rules
```

## Edit by line number

```bash
sudo iptables -L INPUT --line-numbers
sudo iptables -D INPUT 3                          # delete rule 3 from INPUT
sudo iptables -R INPUT 3 -p tcp --dport 22 -j ACCEPT   # replace rule 3
```

## Killer flags / matches

- `-A CHAIN` — append; `-I CHAIN N` — insert at N; `-D` — delete
- `-P CHAIN POLICY` — default policy for the chain
- `-m conntrack --ctstate STATE` — `NEW`, `ESTABLISHED`, `RELATED`, `INVALID`
- `-m multiport --dports 80,443,8080` — multiple ports in one rule
- `-m recent --set / --update --seconds N --hitcount N` — rate limit
- `-j LOG --log-prefix "TAG: "` — log matching packets (sometimes paired with `-m limit`)
- `-t TABLE` — filter (default), nat, mangle, raw
