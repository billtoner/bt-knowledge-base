# glow

Render markdown beautifully in the terminal (a natural pair with `kb show`).

## Use it

```bash
glow README.md                         # render a file with styling
glow -p README.md                      # render inside a pager
glow .                                 # browse the dir's markdown in a TUI
kb show ripgrep | glow -               # render a kb note (reads stdin)
```

## Notes

- `-s dark|light|notty` picks a style; `-w 100` sets the wrap width
- Reads stdin with `-`, so it composes with `kb show`, `curl`, etc.
