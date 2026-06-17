# gpg

Encrypt, sign, and verify; OpenPGP key management.

## Keys

```bash
gpg --full-generate-key                # interactive key creation
gpg --list-secret-keys --keyid-format=long   # secret keys + long IDs
gpg --export -a you@example.com        # export public key (ASCII-armored)
gpg --import pub.asc                    # import a key
```

## Encrypt / decrypt

```bash
gpg -e -r you@example.com file         # encrypt to a recipient
gpg -d file.gpg                         # decrypt to stdout
gpg -c file                             # symmetric (passphrase) encryption
```

## Sign / verify

```bash
gpg --detach-sign -a file              # produce a file.asc signature
gpg --verify file.asc file             # verify a detached signature
gpg --clearsign message.txt            # inline-signed text
```

## Notes

- `--armor`/`-a` makes keys and signatures pasteable ASCII
- Set `GPG_TTY=$(tty)` so pinentry can prompt in the terminal
