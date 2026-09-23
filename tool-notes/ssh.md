# ssh

Secure shell — remote login, remote command execution, port forwarding, file-transfer transport for `scp`/`rsync`/`sftp`. The bedrock.

**Tags:** ssh · remote

## Cool features

- **`~/.ssh/config` aliases everything.** Once `Host prod` is defined, `ssh prod` resolves user, hostname, port, identity, jump host, all of it.
- **`-J` (ProxyJump)** chains through bastions cleanly — `ssh -J bast target` or `ProxyJump bast` in config.
- **Connection multiplexing** (`ControlMaster auto` + `ControlPath` + `ControlPersist`) reuses one TCP+TLS handshake for many sessions. Subsequent connections are sub-second.
- **Three forwarding modes**: `-L` (local→remote port), `-R` (remote→local port), `-D` (SOCKS proxy).
- **`-N -f`** runs ssh as a background tunnel with no remote command — daemonized port-forwarding.
- **`ssh-copy-id`** is the right way to install your pubkey on a server. No more cat-ing into `authorized_keys`.

## Basic

```bash
ssh user@host
ssh user@host 'uname -a'                   # one-shot remote command
ssh -i ~/.ssh/special_key user@host        # specific identity
ssh -p 2222 user@host                      # non-default port
ssh -t user@host 'sudo systemctl status nginx'   # force PTY (for interactive sudo)
```

## Use an SSH config alias

```bash
# In ~/.ssh/config:
#   Host prod
#     HostName 10.0.0.5
#     User deploy
#     IdentityFile ~/.ssh/prod_key
#     Port 2222
#     ServerAliveInterval 60

ssh prod                                   # resolves all of the above
```

## Jump hosts (bastion)

```bash
ssh -J bastion target                       # one hop
ssh -J user1@bast1,user2@bast2 target       # chain through multiple
# Or in ~/.ssh/config:
#   Host target
#     ProxyJump bastion
```

## Port forwarding

```bash
# Local → remote: open port 8080 here, traffic emerges at internal:80 from host's perspective
ssh -L 8080:internal:80 user@host

# Remote → local: open port 9000 on host, traffic emerges at my localhost:9000
ssh -R 9000:localhost:9000 user@host

# SOCKS proxy: route arbitrary local traffic through host
ssh -D 1080 user@host
# Then: curl --socks5-hostname localhost:1080 https://internal-thing/

# Background tunnel (no remote command, fork to background)
ssh -N -f -L 8080:internal:80 user@host
```

## Connection multiplexing (massive speedup)

```bash
# In ~/.ssh/config:
#   Host *
#     ControlMaster auto
#     ControlPath ~/.ssh/cm-%r@%h:%p
#     ControlPersist 10m

# First connect: normal handshake
# Subsequent connects (within 10 min): reuse same TCP — sub-second startup
# `ssh -O check host` — is the master alive?
# `ssh -O exit  host` — close the master connection now
```

## Install your pubkey on a server

```bash
ssh-copy-id user@host                       # default key
ssh-copy-id -i ~/.ssh/prod_key.pub user@host
```

## Known hosts hygiene

```bash
ssh-keygen -R host                          # remove stale fingerprint after rebuild
ssh -o StrictHostKeyChecking=accept-new user@host   # auto-accept first-time, strict after
ssh -o UserKnownHostsFile=/dev/null \
    -o StrictHostKeyChecking=no \
    user@host                               # one-off, no known_hosts mutation (e.g. CI/throwaway VMs)
```

## X11 forwarding (rare but real)

```bash
ssh -X user@host                            # standard
ssh -Y user@host                            # trusted — faster, fewer restrictions, less safe
```

## Generate a new key

```bash
ssh-keygen -t ed25519 -C "you@host"                       # modern default
ssh-keygen -t ed25519 -f ~/.ssh/work_key -C "you@work"    # named key
ssh-keygen -p -f ~/.ssh/old_key                            # change passphrase on existing key
ssh-keygen -y -f ~/.ssh/key                                # print pubkey from priv
ssh-keygen -lf ~/.ssh/key.pub                              # fingerprint
```

## Debug auth / connection issues

```bash
ssh -v user@host                            # auth flow
ssh -vv user@host                           # + crypto/kex
ssh -vvv user@host                          # full transport debugging
ssh -G user@host                            # show effective config for a host (no connect)
```

## Useful `~/.ssh/config` patterns

```
# Defaults for everything
Host *
    AddKeysToAgent yes
    UseKeychain yes                         # macOS keychain
    ServerAliveInterval 60                  # keep flaky NAT alive
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlPersist 10m

# Named host
Host prod
    HostName 10.0.0.5
    User deploy
    IdentityFile ~/.ssh/prod_key
    Port 2222

# Wildcard hosts behind a bastion
Host *.internal
    ProxyJump bastion.example.com
    User deploy

# GitHub shortcut
Host gh
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

## Killer flags

- `-i <key>` — identity file
- `-p <port>` — non-default port
- `-J <jump>` — jump through bastion(s)
- `-L <local>:<host>:<port>` — local→remote forward
- `-R <remote>:<host>:<port>` — remote→local forward
- `-D <port>` — SOCKS proxy
- `-N -f` — background tunnel, no remote command
- `-t` — force PTY (interactive sudo, etc.)
- `-A` — agent forwarding (use sparingly, security risk)
- `-G` — print effective config without connecting
- `-o '<Option>=<value>'` — override any config setting per-invocation
