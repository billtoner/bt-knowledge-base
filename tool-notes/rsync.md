# rsync

Block-level file sync over SSH or local paths. Fast on repeat runs because it only transfers what changed. The trailing-slash rule is the one thing to memorize.

**Tags:** files · sync · remote

## The trailing-slash rule

```bash
rsync -av source/  dest/    # copy CONTENTS of source/ into dest/        → dest/file1, dest/file2
rsync -av source   dest/    # copy source itself into dest/              → dest/source/file1, dest/source/file2
```

This trips everyone up. Always check.

## Cool features

- **`--link-dest`** hardlinks unchanged files from a previous snapshot. Time Machine–style backups with negligible disk overhead.
- **`--partial --append-verify`** resumes after a dropped connection — picks up where the last byte landed and verifies.
- **`-n` (dry run)** is the most-used flag you'll forget. Always practice destructive runs with it first.

## Local copies

```bash
rsync -av source/ dest/                           # archive: recursive, perms, times, symlinks, etc.
rsync -avh --progress source/ dest/               # human-readable sizes + per-file progress
rsync -avn source/ dest/                          # DRY RUN — list what would be transferred
```

## Over SSH (most common production use)

```bash
rsync -avzhP source/ user@host:/path/             # compress + progress; the everyday remote sync
rsync -avzhP -e 'ssh -p 2222' src/ user@host:/dst/    # non-standard SSH port
rsync -avzhP --rsh='ssh -i ~/.ssh/deploy_key' src/ user@host:/dst/
```

## Make `dest` match `source` exactly

```bash
rsync -avz --delete --delete-excluded source/ dest/
                                                  # files in dest that aren't in source get removed
                                                  # ALWAYS run with -n first
```

## Excludes

```bash
rsync -avz --exclude='*.log' --exclude='.git' source/ dest/
rsync -avz --exclude-from=.rsyncignore source/ dest/
```

## Resume a fat transfer that dropped

```bash
rsync -avhP --partial --append-verify source.iso user@host:/big/
                                                  # safe to rerun the exact same command
                                                  # already-uploaded bytes are verified, not re-sent
```

## Snapshot-style backups (--link-dest)

```bash
rsync -av --delete --link-dest=../snapshot.0/ source/ snapshot.1/
                                                  # snapshot.1 looks like a full copy
                                                  # but unchanged files are hardlinks to snapshot.0
                                                  # → near-zero extra disk usage per snapshot
```

## Throttle / nice runs

```bash
rsync -avz --bwlimit=10M source/ dest/            # cap at 10 MB/s
ionice -c 3 nice rsync -avz source/ dest/         # be polite to disks and CPU
```

## Killer flags

- `-a` — archive (`-rlptgoD`); the default starting point
- `-v` — verbose; `-vv` for more, `-vvv` for too much
- `-z` — compress over the wire
- `-h` — human-readable sizes
- `-P` — `--partial --progress` in one flag
- `-n` — dry run
- `--delete` — remove files from dest that aren't in source
- `--exclude` / `--exclude-from` — skip patterns
- `--link-dest=DIR` — hardlink unchanged files from DIR (snapshot backups)
- `--bwlimit=N` — cap throughput (KB/s by default; `M`/`G` suffixes work)
- `--append-verify` — resume + verify already-transferred bytes
