# ncdu

Interactive "what's eating my disk" — a navigable `du` (with `dust` for a quick tree).

## Use it

```bash
ncdu /                                 # scan a tree, then browse interactively
ncdu -x /                              # stay on one filesystem (skip other mounts)
ncdu -o scan.json /data                # save a scan to a file
ncdu -f scan.json                      # browse a saved scan (no rescan)
```

## In-TUI keys

- arrows navigate; `d` delete the selected item; `n`/`s` sort by name/size
- `g` toggle percent/graph; `i` info; `r` rescan

## dust (one-shot tree)

```bash
dust                                   # biggest dirs under cwd, as a tree
dust -d 3 /var                         # limit depth
```

## Notes

- `ncdu -x` is the right call on a server — don't descend into other mounts/NFS
- `dust` needs no interaction; great for a quick "where did the space go"
