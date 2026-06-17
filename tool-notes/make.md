# make

The ubiquitous build/task runner; targets, prerequisites, parallelism.

## Running

```bash
make                                   # build the first (default) target
make test                              # run a named target
make -j8                               # run up to 8 jobs in parallel
make -n install                        # dry-run: print recipes, don't execute
make -B                                # force rebuild, ignoring timestamps
```

## Debugging a Makefile

```bash
make -p                                # dump the database: rules + variables
make --trace                           # show why each recipe fires
make VAR=value target                  # override a variable from the CLI
```

## Notes

- Recipe lines start with a TAB, never spaces (the classic gotcha)
- Automatic vars: `$@` target, `$<` first prereq, `$^` all prereqs
- `.PHONY: test build clean` for targets that aren't files
