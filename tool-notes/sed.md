# sed

Stream editing; substitutions, address ranges, in-place edits.

## Substitute

```bash
sed 's/old/new/' file                   # first match per line
sed 's/old/new/g' file                  # all matches
sed -E 's/([a-z]+)=([0-9]+)/\2:\1/' f   # extended regex + backreferences
sed 's#/usr/local#/opt#g' file          # alt delimiter to avoid escaping /
```

## Addresses & ranges

```bash
sed -n '10,20p' file                    # print lines 10-20 (a slice)
sed '/^#/d' file                        # delete comment lines
sed '/START/,/END/d' file               # delete an inclusive range
sed -n '/ERROR/{p;n;p}' log             # a matching line and the next one
```

## In-place

```bash
sed -i 's/foo/bar/g' file               # edit in place (GNU)
sed -i.bak 's/foo/bar/g' file           # ...keeping a .bak backup
sed -i '' 's/foo/bar/g' file            # BSD/macOS: empty suffix = no backup
```

## Notes

- `-E` for extended regex; `-n` suppresses auto-print (pair with `p`)
- macOS `sed -i` needs an argument (`-i ''`); GNU sed does not
