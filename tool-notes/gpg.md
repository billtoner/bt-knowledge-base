# gpg

Encrypt, sign, and verify; OpenPGP key management.

**Tags:** crypto · secrets

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

## Password-encrypt one file (no keys)

Symmetric: a passphrase is the only thing needed to open it — nothing to share, no keyring.

```bash
gpg -c secret.pdf                       # prompts twice, writes secret.pdf.gpg
rm secret.pdf                           # original is still plaintext — delete once verified
gpg secret.pdf.gpg                      # decrypt: prompts, restores secret.pdf
gpg -d secret.pdf.gpg > out.pdf         # decrypt to a name you pick
```

- Lose the passphrase → the file is gone. Use a typeable random-word passphrase (Tier 0 style).

### "It decrypted without asking for the password"

gpg-agent **caches the passphrase** (~10 min, up to 2 h) after you encrypt/decrypt — so a soon-after decrypt skips the prompt. The file is fine. To force a prompt:

```bash
gpgconf --reload gpg-agent              # flush cached passphrases (or --kill to restart)
gpg -d secret.pdf.gpg > /dev/null       # should prompt now; tests without writing
```

Still no prompt after flushing? Confirm it's actually symmetric:

```bash
gpg --list-packets secret.pdf.gpg | head
# "symkey enc packet" → passphrase-encrypted (gpg -c)
# "pubkey enc packet"  → encrypted to a key; YOUR private key is opening it
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
