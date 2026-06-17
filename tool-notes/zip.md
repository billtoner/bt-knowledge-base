# zip

ZIP archives for cross-platform interop (zip / unzip).

## Create

```bash
zip -r out.zip dir/                     # recurse a directory
zip out.zip a.txt b.txt                 # specific files
zip -r out.zip dir/ -x '*.log'          # exclude a pattern
zip -e private.zip file                 # encrypt (prompts for a password)
```

## Inspect / extract

```bash
unzip -l out.zip                        # list contents
unzip out.zip -d /target                # extract into a directory
unzip -o out.zip                        # overwrite without prompting
unzip -j out.zip                        # junk paths (flatten)
```

## Notes

- Use ZIP for interop (Windows/macOS); tar+zstd/xz for Unix-to-Unix
- ZIP's built-in encryption is weak — prefer gpg/age or 7z AES for real secrecy
