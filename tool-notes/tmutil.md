# tmutil (`tmutil` / `diskutil`)

Time Machine command reference for the two-HDD backup strategy: the `tmutil` /
`diskutil` commands used setting up and operating encrypted APFS backups.

**Tags:** macos · backup · disk

Commands used setting up and operating the two-HDD Time Machine strategy
(encrypted APFS **Backup-ADATA** primary + reformatted **My Passport** as the
rotating offsite drive). Grouped by task, with the caveats that actually bit us.

Legend: 🔎 read-only/safe · 🔐 needs `sudo` · ⚠️ destructive or state-changing

> **`sudo` needs a real TTY.** Running these via a non-interactive shell (e.g.
> Claude Code's `!` prefix) fails with *"a terminal is required to read the
> password."* Run `sudo` lines in a normal terminal window.

---

## 1. Inspect drives & state (🔎 read-only, no sudo)

```sh
diskutil list external physical          # external disks + partition scheme/format
diskutil list /dev/disk8                 # one disk's layout
diskutil info /dev/disk8                 # size, type, SMART status (USB = "Not Supported")
diskutil apfs list                       # APFS containers/volumes incl. FileVault (encryption) state
df -h | grep -i backup-adata             # capacity / % used of a mounted volume
mount | grep -i backup-adata             # where a volume is actually mounted
```

Key fields to read:
- `Apple_HFS` = HFS+ (legacy, slow for TM) · `Apple_APFS` = APFS (what we want).
- `FileVault: Yes (Unlocked)` = encrypted + currently unlocked.

## 2. Time Machine status (🔎 read-only)

```sh
tmutil destinationinfo                   # configured backup destinations (name/kind/mount/ID)
tmutil destinationinfo -X                # same, as XML plist (parseable)
tmutil currentphase                      # e.g. Copying, BackupNotRunning
tmutil status                            # live progress dict (BackupPhase, Percent, bytes...)
tmutil latestbackup                      # path of newest completed backup (errors if none yet)
tmutil listbackups -d "/Volumes/<drive>" # list all backups on a mounted destination
```

Richer per-destination data (RESULT code, BytesUsed/Available, encryption state,
filesystem type, snapshot dates) lives in the prefs plist — **readable without sudo**:

```sh
defaults export /Library/Preferences/com.apple.TimeMachine.plist -   # full prefs as XML
defaults read   /Library/Preferences/com.apple.TimeMachine.plist     # same, old-style
```

Failure reasons from the unified log (predicate that filters out non-TM noise):

```sh
log show --last 3d --style compact \
  --predicate 'process == "backupd" AND (eventMessage CONTAINS[c] "ackup" \
    OR eventMessage CONTAINS[c] "destination" OR eventMessage CONTAINS[c] "snapshot" \
    OR eventMessage CONTAINS[c] "mount")'
```
Note: `RESULT = 0` in the prefs plist means the last backup succeeded; nonzero is
an error code (e.g. `47 = BACKUP_FAILED_NO_SUCH_DESTINATION`).

## 3. Format a new backup drive (⚠️ destructive)

```sh
# Plain APFS (fine if you'll encrypt via the Time Machine toggle — see §5):
diskutil eraseDisk APFS  "Backup-ADATA" GPT /dev/disk8

# Mac OS Extended / HFS+ — used to FORCE Time Machine's reformat+encrypt flow (§5):
diskutil eraseDisk JHFS+ "Backup-ADATA" GPT /dev/disk8
```
`eraseDisk` wipes the WHOLE disk (removes Windows/Microsoft partitions too).
**Double-check the `/dev/diskN` — target the new drive, not your Passport.**

## 4. Manage destinations & run backups (🔐 sudo)

```sh
sudo tmutil setdestination  /Volumes/Backup-ADATA     # set as THE destination (replaces list)
sudo tmutil setdestination -a /Volumes/<drive>        # APPEND a destination (keep others)
sudo tmutil removedestination <DEST-ID>               # de-register (does NOT erase data)
sudo tmutil startbackup                               # start a backup now
sudo tmutil stopbackup                                # stop the running backup
sudo tmutil enable                                    # turn automatic backups ON
sudo tmutil disable                                   # turn automatic backups OFF
```
Get `<DEST-ID>` from `tmutil destinationinfo`. For two-drive rotation, add both
with `setdestination -a`.

## 5. Encrypted Time Machine — the recipe that works ⭐

The encrypt toggle only appears when Time Machine has to **reformat** a disk, i.e.
when you add a **non-APFS** disk. So:

```sh
# 1. de-register any existing dest + erase to NON-APFS to force the reformat flow
sudo tmutil removedestination <DEST-ID>
diskutil eraseDisk JHFS+ "Backup-ADATA" GPT /dev/disk8
# 2. System Settings > Time Machine > + > Set Up Disk > toggle "Encrypt Backup Disk" ON > password
# 3. HANDS OFF — let Time Machine reformat to APFS (Encrypted), store the key, and start.
```

**Do NOT:**
- pre-encrypt in Finder / Disk Utility — the key lands in your *login* keychain,
  not the *system* keychain, so `backupd` can't unlock the drive.
- manually `diskutil unmount` / `diskutil apfs unlockVolume` / eject a live TM
  destination — that desyncs `backupd` and causes **Code 17 "Failed to mount
  destination"** even when the volume is mounted & unlocked. Let `backupd` mount
  and unlock it itself.

If you ever need to unlock an APFS volume by hand (NOT a live TM dest):
```sh
diskutil apfs unlockVolume disk9s2        # prompts for passphrase (or uses keychain)
```

A volume mounting as `/Volumes/<name> 1` (trailing " 1") is cosmetic — `backupd`
tracks by volume UUID. Don't "fix" it by unmounting.

## 6. Exclusions & retention (from the right-sizing work)

```sh
tmutil isexcluded <path>                  # 🔎 is a path excluded?
sudo tmutil addexclusion <path>           # 🔐 sticky (xattr on the item) — LOST if dir is recreated
sudo tmutil addexclusion -p <path>        # 🔐 path-based (system prefs) — survives recreation
sudo tmutil removeexclusion [-p] <path>   # 🔐 undo
tmutil delete -p "/Volumes/<drive>/.../<backup>"   # 🔐 delete a specific backup (this macOS: -p form only)
```
Use `-p` (path-based) for anything that gets deleted/recreated (e.g.
`node_modules`) and for managed paths like `~/Library/Mobile Documents` (iCloud),
where the sticky form fails with Error -20.

## 7. Restore

See **[tm-restore](tm-restore.md)** (or `tm-health restore`). Core command:
```sh
tmutil restore -v "<path-inside-a-backup>" "<destination>"
```

---
*Companion tools in this repo: `tm-health` (dashboard), [tm-restore](tm-restore.md) (restore guide).*
