# scp

Copy files between hosts over SSH. Same auth, same `~/.ssh/config`, same known_hosts as `ssh`.

**Tags:** ssh · remote · files

## Cool features

- **Uses SSH end-to-end.** Any host you can `ssh` to, you can `scp` to — including `~/.ssh/config` aliases.
- **`-3` routes remote-to-remote through your machine.** Useful when the two remotes can't SSH to each other directly but both let you in.
- **`-C` compresses in transit.** Big text payloads over slow links benefit a lot.
- **`-l <Kbit/s>` caps bandwidth.** Polite when copying large files from a shared server.
- **IPv6 needs brackets.** `scp file '[user@2001:db8::1]:/path'` — without brackets, the `:` parses wrong.
- **OpenSSH 9.0+ uses SFTP under the hood.** If a server only supports the legacy SCP protocol, force it with `-O`.

## Basic copies

```bash
scp file.txt user@host:/remote/path/                # local → remote
scp user@host:/remote/file.txt .                    # remote → local
scp user@host:/path/'*.log' .                       # quote globs — they expand on the remote
scp file1.txt file2.txt user@host:/path/            # multiple sources
```

## Directories

```bash
scp -r ./dir user@host:/path/                       # recursive
scp -rp ./dir user@host:/path/                      # recursive + preserve mtime/perms
```

## Between two remote hosts

```bash
scp user1@host1:/path/file user2@host2:/path/       # default: direct host1↔host2
scp -3 user1@host1:/path/file user2@host2:/path/    # route through this machine
```

## Non-default port / identity

```bash
scp -P 2222 file.txt user@host:/path/               # custom port (capital P — ssh uses lowercase)
scp -i ~/.ssh/special_key file.txt user@host:/path/ # specific key
```

## Use an SSH config alias

```bash
# In ~/.ssh/config:
#   Host prod
#     HostName 10.0.0.5
#     User deploy
#     IdentityFile ~/.ssh/prod_key

scp file.txt prod:/srv/app/                         # alias resolves user, host, key, port
```

## Tuning the transfer

```bash
scp -C file.txt user@host:/path/                    # compress
scp -l 1000 file.txt user@host:/path/               # cap at 1000 Kbit/s
scp -q file.txt user@host:/path/                    # quiet — suppress progress meter
scp -v file.txt user@host:/path/                    # verbose for debugging auth/connection
```

## When the server is old

```bash
scp -O file.txt user@host:/path/                    # force legacy SCP protocol (OpenSSH 9.0+ default is SFTP)
scp -T file.txt user@host:/path/                    # disable strict filename checking
```

## Habit shifts — scp vs alternatives

| Need | Tool |
|---|---|
| One-off file, small | `scp` |
| Resumable, partial, mirror | `rsync -aP --partial` |
| Delete remote files not on local | `rsync --delete` |
| Interactive browse + transfer | `sftp` |

## Killer flags

- `-r` — recursive (copy directories)
- `-p` — preserve modification times and permissions
- `-P <port>` — non-default SSH port (**capital P** — easy to confuse with ssh's lowercase)
- `-i <key>` — specific identity file
- `-3` — route remote-to-remote through this machine
- `-C` — compression
- `-O` — force legacy SCP protocol
