# broot

Interactive tree navigator with fuzzy search and built-in file actions.

## Use it

```bash
br                                     # launch via the shell-function wrapper
broot                                  # launch directly
broot -s                               # show sizes, sorted
broot -h                               # include hidden files
```

## In-app

- type to fuzzy-filter; `Enter` to open/`cd`; `:` runs a verb
- `:cp`, `:mv`, `:rm`, `/` to search contents, `Alt-Enter` to `cd` there

## Notes

- Install the `br` shell function so quitting can `cd` your shell into the chosen dir
- Verbs (`:`) are configurable; great for navigating large trees by keyword
