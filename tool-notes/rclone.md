# rclone

`rsync` for cloud storage — sync, copy, and mount 70+ providers (Google Drive,
S3, Dropbox, …) from one CLI. These examples assume a remote named `gdrive`.

**Tags:** cloud · sync · files · gcp

## Cool features

- **Mount a remote as a local filesystem.** `rclone mount` exposes Drive as a folder you can `cd` into and open in Finder.
- **Server-side transfers.** Copying between two Google Drive remotes moves data cloud-to-cloud without downloading it to your machine.
- **Crypt overlay.** Wrap any remote in an encrypted layer so filenames and contents are encrypted before upload.
- **`--dry-run` everywhere.** Every destructive command previews first — nothing moves until you drop the flag.

## One-time setup

```bash
rclone config                          # interactive wizard: add a "gdrive" remote
rclone listremotes                     # show configured remotes
rclone about gdrive:                   # quota: used / free / total on the Drive
```

The wizard walks through OAuth in the browser; pick `drive` as the type. For a
headless box, choose "no" at the auto-config step and paste the token from
another machine.

## Browse & inspect

```bash
rclone ls gdrive:                      # recursive: every file with size
rclone lsd gdrive:                     # directories only, one level
rclone lsf gdrive:Photos/             # bare file names in a folder
rclone tree gdrive:Projects           # visual tree of a folder
rclone size gdrive:Backups            # total size + object count of a path
```

## Copy & sync

```bash
rclone copy ./localdir gdrive:Backups/localdir   # upload (additive, never deletes)
rclone copy gdrive:Reports ./reports             # download a folder
rclone sync ./site gdrive:site --dry-run         # preview mirror (deletes extras!)
rclone sync ./site gdrive:site                   # mirror local -> Drive
rclone copy gdrive:a-remote: gdrive2:backup      # server-side, no local download
```

`copy` only adds/updates; `sync` makes the destination match the source and
**deletes** files not present in the source. Always `--dry-run` a `sync` first.

## Move, delete, single files

```bash
rclone copyto ./report.pdf gdrive:Docs/2026-report.pdf   # rename on upload
rclone move ./done gdrive:Archive/done                   # upload then delete source
rclone deletefile gdrive:Docs/old.pdf                    # one file
rclone delete gdrive:tmp --min-age 30d                   # files older than 30 days
rclone purge gdrive:Trash                                # remove a dir and contents
```

## Mount as a local folder

```bash
mkdir -p ~/gdrive
rclone mount gdrive: ~/gdrive --vfs-cache-mode writes   # foreground; Ctrl-C to unmount
rclone mount gdrive: ~/gdrive --daemon                  # background
```

`--vfs-cache-mode writes` (or `full`) is what makes editing files in place work
reliably — without it, apps that reopen a file mid-write can fail.

## Google Drive specifics

```bash
rclone copy gdrive:Sheet.gsheet ./ \
  --drive-export-formats xlsx,csv               # export native Google formats
rclone lsjson gdrive:Shared --drive-shared-with-me   # files shared with you
rclone copy "gdrive,root_folder_id=ABC123:" ./dl     # scope to one folder id
rclone dedupe gdrive:                            # Drive allows dup names; merge them
```

Google Docs/Sheets/Slides have no real file size and can't be copied byte-for-byte
— they must be exported (`--drive-export-formats`) or they're skipped.

## Killer flags

- `--dry-run` — preview any transfer/delete before it happens
- `-P` / `--progress` — live transfer stats (speed, ETA, %)
- `--transfers N` — parallel file transfers (default 4; raise for many small files)
- `--fast-list` — one bulk listing instead of per-dir calls; fewer API hits on big trees
- `--drive-export-formats` — how to download native Google Docs/Sheets
- `--vfs-cache-mode writes` — required for sane read/write on `rclone mount`
