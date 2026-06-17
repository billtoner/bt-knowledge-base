# zstd

Fast modern compression; great ratios at high speed, with tunable levels.

## Compress / decompress

```bash
zstd file                               # -> file.zst (keeps the original)
zstd -d file.zst                        # decompress (or: unzstd)
zstd -19 file                           # max standard ratio (slow); -1 fastest
zstd --rm file                          # compress and remove the original
```

## Big jobs

```bash
zstd -T0 -19 big.bin                     # use all cores
zstd --long=27 huge.bin                  # long-range matching for large inputs
tar --zstd -cf out.tar.zst dir/          # tar + zstd in one step
```

## Notes

- Levels 1-19 (plus `--ultra -22`); ~level 3 is a great speed/ratio default
- `-T0` uses all cores; decompression is fast at any level
