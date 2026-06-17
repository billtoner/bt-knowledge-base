# pass

The standard Unix password store; gpg-encrypted files in a git repo.

## Daily use

```bash
pass                                    # tree of all entries
pass show github/token                  # print an entry
pass -c github/token                    # copy to clipboard (auto-clears after 45s)
pass insert github/token                # add interactively (hidden input)
pass generate github/token 24           # generate + store a 24-char password
```

## Sync & search

```bash
pass git push                           # the store is a git repo
pass grep PATTERN                       # search decrypted contents
pass edit github/token                  # edit in $EDITOR
```

## Notes

- Each entry is a gpg-encrypted file under `~/.password-store`
- Set up: `pass init <gpg-id>`, then `pass git init` to track it in git
