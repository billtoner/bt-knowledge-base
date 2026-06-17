# tar

Create and extract archives; the flags you always re-look-up.

## Create / extract

```bash
tar czf out.tgz dir/                    # create, gzip-compressed
tar xzf out.tgz                         # extract gzip
tar xzf out.tgz -C /target              # extract into a directory
tar tzf out.tgz                         # list contents (no extract)
```

## Compression variants

```bash
tar caf out.tar.zst dir/                # auto-pick compressor from the extension
tar cJf out.tar.xz dir/                 # xz
tar --zstd -cf out.tar.zst dir/         # explicit zstd
```

## Selective & transforms

```bash
tar xzf a.tgz path/inside               # extract just one path
tar czf out.tgz --exclude='*.log' dir/  # exclude a pattern
tar czf out.tgz --transform 's,^,prefix/,' dir/   # rewrite paths on the fly
```

## Notes

- Mnemonics: c=create, x=extract, t=list; f=file, v=verbose; z/J/j/--zstd = compressor
- `-a` (or `caf`) auto-selects the compressor from the output filename
