# go

The Go toolchain; build, test, run, modules, vet. (For quick snippets, see
go-one-liners under Languages & Scripting.)

## Build / run / test

```bash
go run .                               # compile + run the current package
go build ./...                         # build everything
go test ./... -run TestName -v         # run matching tests, verbose
go test -race -cover ./...             # race detector + coverage
go vet ./...                           # static checks
```

## Modules

```bash
go mod init example.com/m              # start a module
go mod tidy                            # add missing, drop unused deps
go get -u ./...                        # upgrade dependencies
go list -m all                         # full dependency graph
```

## Tooling & cross-compile

```bash
go install golang.org/x/tools/cmd/stringer@latest   # install a tool
GOOS=linux GOARCH=arm64 go build       # trivial cross-compilation
go test -bench=. -benchmem ./...        # benchmarks
```

## Notes

- `go env GOPATH GOMODCACHE` shows toolchain paths
- `gofmt -w .` (or `go fmt ./...`) for canonical formatting
