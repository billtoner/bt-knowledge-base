# go-one-liners

Quick Go from the shell; `go run`, docs, and run-a-tool-without-installing.

## Run & docs

```bash
go run .                               # compile + run the current package
go run main.go                         # run a single file
go doc strings.Builder                 # stdlib docs in the terminal
go doc -src fmt.Println                # ...with the source
```

## Run tools without installing

```bash
go run golang.org/x/tools/cmd/godoc@latest -http=:6060   # local docs server
go run github.com/rakyll/hey@latest -n 1000 -c 50 http://localhost:8080   # quick load test
gofmt -d .                             # show formatting diffs without writing
```

## Notes

- For build/test/modules, see the `go` note under Build & Packaging
- `go run <pkg>@latest` runs a tool without installing it (like npx / uvx)
