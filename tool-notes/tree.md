# tree

Recursive directory listing as a tree.

## Use it

```bash
tree -L 2                              # limit depth to 2 levels
tree -a                                # include hidden files
tree -d                                # directories only
tree -I 'node_modules|.git'            # ignore matching names
```

## Output

```bash
tree -h                                # show file sizes
tree --gitignore                       # respect .gitignore
tree -J                                # JSON output
tree -P '*.py'                         # only files matching a pattern
```

## Notes

- `-I 'a|b'` prunes noise (node_modules/.git); `-L N` keeps it readable
- `eza --tree` is a modern alternative that adds git status (see eza)
