# pass

The standard Unix password store — each entry a gpg-encrypted file, plaintext on demand from the CLI.

**Tags:** passwords · secrets · crypto · keys

## Cool features

- **Plaintext on demand, ciphertext at rest.** `pass show x` prints it, but the file on disk is gpg-encrypted — no plaintext working copy (unlike git-crypt, which decrypts the whole tree).
- **Clipboard with auto-clear.** `pass -c x` copies and wipes the clipboard after ~45s, keeping secrets out of terminal scrollback.
- **Just files + gpg + (optional) git.** The whole store is `~/.password-store`; each entry a `.gpg` file in a tab-completable tree.

## Setup (macOS)

```bash
brew install pass gnupg pinentry-mac
echo "pinentry-program /opt/homebrew/bin/pinentry-mac" >> ~/.gnupg/gpg-agent.conf
gpgconf --kill gpg-agent                # passphrase prompts now a Mac GUI dialog
gpg --full-generate-key                 # run in a REAL terminal (needs a TTY); ed25519, strong passphrase
pass init <gpg-fingerprint-or-email>    # creates ~/.password-store
```

## Daily use

```bash
pass                                    # tree of all entries
pass show personal/gmail                # print plaintext (first decrypt → passphrase dialog)
pass -c personal/gmail                  # copy line 1 (the password) to clipboard (auto-clears ~45s)
pass -c2 personal/gmail                 # copy line 2 (e.g. the username) — -cN copies the Nth line
pass personal/gmail | sed -n 's/^login: //p'   # extract a named field by script
pass insert personal/gmail              # add interactively (hidden input)
pass insert -m aws/root                 # multiline: password line 1, user/url/notes below
pass generate personal/wifi 24          # generate + store a 24-char password
pass edit personal/gmail                # decrypt → $EDITOR → re-encrypt
pass rm personal/gmail                  # delete an entry
pass grep PATTERN                       # search decrypted contents
```

Convention: **first line = the password** (that's what `-c` copies); put `user:`, `url:`, notes on the lines below. `pass -c2` then copies the username.

## Store more than passwords

Entries are arbitrary text, so `pass` holds any secret — API tokens, keys, codes:

```bash
pass insert -m api/openai                     # paste the token (+ notes), Ctrl-D
export OPENAI_API_KEY="$(pass show api/openai | head -1)"   # into the env, never hardcoded

pass insert -m ssh/id_ed25519 < ~/.ssh/id_ed25519          # store a text key file (stdin)
pass show ssh/id_ed25519 > ~/.ssh/id_ed25519               # restore it
chmod 600 ~/.ssh/id_ed25519

base64 -i secret.bin | pass insert -m notes/secret-b64     # binary secret → base64 first
pass show notes/secret-b64 | base64 -d > secret.bin        # restore
```

Organize the tree so it's not just logins: `personal/` (user+pass) · `api/` (tokens) ·
`aws/` (keys) · `ssh/` · `notes/` (recovery codes, licenses, wifi). `pass insert -m aws/personal`
creates the folder automatically; `pass find <term>` searches entry names.

## Back up the key — it's the single point of failure

```bash
gpg --export-secret-keys --armor <fpr> > pwkey-private.asc   # store OFFLINE / in a vault
# restore on a new machine: gpg --import pwkey-private.asc
```

- Lose the gpg private key → **every entry is unrecoverable**.
- Entry **contents** are encrypted, but **names/paths are not** (`banks/chase` leaks the account) — so `pass git push` to a **private remote only**, never public.
- Prefer `-c` over `show` to keep plaintext out of scrollback; `gpg-agent` caches the passphrase (~10 min; tune with `default-cache-ttl` in `gpg-agent.conf`).
- Keep `pass` as a CLI subset; Apple Passwords stays the main vault. Don't auto-sync — pick which holds each entry.

## Killer flags

- `-c` — copy to clipboard instead of printing (auto-clears)
- `-cN` — copy the Nth line (e.g. `-c2` for the username)
- `-m` — multiline insert (password + metadata)
- `generate -n` — no symbols in the generated password
- `-f` — force (skip the overwrite / delete prompt)
