# ufw (Uncomplicated Firewall)

Ubuntu's friendly frontend over iptables/nftables. Optimized for "I just want SSH and HTTPS open and everything else closed."

**Tags:** firewall · network

## Cool features

- **`ufw limit`** rate-limits brute-force attempts with one word. (Underneath: `6 conns / 30s` per source → drop.)
- **App profiles** (`ufw allow 'OpenSSH'`) name common services. `ufw app list` shows what your system knows.
- **`ufw status verbose`** shows defaults, logging level, and rules in one glance.

## Day-one setup

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH                            # **before** ufw enable — don't lock yourself out
sudo ufw enable                                   # warns if no SSH allow exists
sudo ufw status verbose
```

## Add / remove rules

```bash
sudo ufw allow 22/tcp                             # simple form
sudo ufw allow ssh                                # by /etc/services name
sudo ufw allow 'OpenSSH'                          # by named app profile
sudo ufw allow from 10.0.0.0/8 to any port 22     # restrict source
sudo ufw allow proto tcp from any to any port 80,443
                                                  # multiple ports in one rule

sudo ufw deny 23/tcp                              # explicit deny
sudo ufw deny from 192.0.2.7                      # block a bad actor outright

sudo ufw status numbered                          # see rule numbers
sudo ufw delete 3                                 # delete rule by number
sudo ufw delete allow 22/tcp                      # or by exact match
```

## Rate-limit SSH (the one-word version)

```bash
sudo ufw limit 22/tcp                             # >6 conns / 30s from one IP → drop
```

## App profiles

```bash
sudo ufw app list                                 # what profiles are installed?
sudo ufw app info 'OpenSSH'                       # what ports does it open?
```

## Reset / disable

```bash
sudo ufw reset                                    # nukes all rules; prompts for confirmation
sudo ufw disable                                  # stop filtering (rules preserved)
```

## When to reach past ufw

ufw is a thin wrapper. For NAT, complex chains, conntrack states, or anything beyond "allow / deny a port," drop down to `nft` or `iptables` directly.
