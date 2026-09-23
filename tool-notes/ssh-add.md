# ssh-add

Load, list, and unload private keys in the running `ssh-agent`. The agent decrypts the key once (you type the passphrase) and ssh reuses it without re-prompting.

**Tags:** ssh · keys

## Cool features

- **`ssh-add` with no args loads the default identities** (`~/.ssh/id_rsa`, `~/.ssh/id_ed25519`, etc.).
- **`-L` prints the loaded pubkeys in OpenSSH format** — paste-ready for GitHub/GitLab/authorized_keys.
- **`-t <seconds>` sets a lifetime** — agent forgets the key after N seconds. Great for transient access on shared machines.
- **macOS `--apple-use-keychain`** stores the passphrase in the macOS Keychain, so the agent re-loads it silently on login without prompting.
- **`AddKeysToAgent yes`** in `~/.ssh/config` makes ssh auto-add keys to the agent on first use — no need to remember `ssh-add` at all.

## Load (add) keys

```bash
ssh-add                              # load default identities (~/.ssh/id_*)
ssh-add ~/.ssh/special_key           # specific key — prompts for passphrase if set
ssh-add -t 3600 ~/.ssh/temp_key      # forget after 1 hour
```

## List

```bash
ssh-add -l                           # loaded keys, fingerprints
ssh-add -L                           # loaded keys, full pub format (paste into GitHub etc.)
```

## Remove

```bash
ssh-add -d ~/.ssh/special_key        # remove one
ssh-add -D                           # remove ALL keys from the agent
```

## macOS Keychain (persist passphrase across reboots)

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519     # save passphrase to Keychain

# Then in ~/.ssh/config:
#   Host *
#     AddKeysToAgent yes
#     UseKeychain yes
#     IdentityFile ~/.ssh/id_ed25519
# → ssh will load + unlock automatically on first use, forever.
```

## Verify the agent is running

```bash
echo "$SSH_AUTH_SOCK"                # should print a socket path; empty = no agent
ssh-add -l                           # "Could not open a connection..." = no agent
eval "$(ssh-agent -s)"               # start a new agent in current shell
ssh-agent -k                         # kill the agent referenced by SSH_AUTH_SOCK
```

## Killer flags

- `-l` — list loaded keys (fingerprints)
- `-L` — list loaded keys (full pub format)
- `-d <key>` — remove one key
- `-D` — remove all keys
- `-t <secs>` — load with lifetime
- `--apple-use-keychain` — macOS: persist passphrase in Keychain
