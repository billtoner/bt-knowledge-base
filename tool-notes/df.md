# df

Filesystem free space (`df`) and per-directory usage (`du`).

## df — free space

```bash
df -h                                  # human sizes, all filesystems
df -h /data                            # the filesystem backing a path
df -hT                                 # include the filesystem type
df -i                                  # inode usage (the "full" that isn't bytes)
```

## du — what's using it

```bash
du -sh *                               # size of each item in cwd
du -h -d1 /var | sort -h               # one level deep, sorted
du -xsh /                              # one filesystem only
```

## Notes

- `df -i` catches "No space left" when inodes are exhausted but bytes aren't
- For interactive drill-down use `ncdu`; `du | sort -h` for a quick one-shot
