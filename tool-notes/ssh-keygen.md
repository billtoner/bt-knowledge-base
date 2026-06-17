# ssh-keygen

Create, convert, and inspect SSH keys; fingerprints and host-key management.

## Make keys

```bash
ssh-keygen -t ed25519 -C "me@host"     # the modern default key type
ssh-keygen -t ed25519 -f ~/.ssh/id_work   # a separate key for one context
ssh-keygen -p -f ~/.ssh/id_ed25519     # change a key's passphrase
```

## Fingerprints & known_hosts

```bash
ssh-keygen -lf ~/.ssh/id_ed25519.pub   # fingerprint of a key
ssh-keygen -R hostname                 # drop a host from known_hosts (after a rekey)
ssh-keygen -y -f ~/.ssh/id_ed25519     # derive the public key from a private key
```

## Notes

- Prefer `ed25519`; use `-t rsa -b 4096` only where ed25519 isn't supported
- Load the new key with `ssh-add`; `-a 100` raises the KDF rounds for the passphrase
