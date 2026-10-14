# tm-restore (`tmutil restore`)

Restoring from Time Machine — a file, a folder, or the whole machine — for the
two-drive encrypted-APFS backup setup. Companion to [tmutil](tmutil.md).

**Tags:** macos · backup · disk

This is the restore reference for the two-drive Time Machine setup
(**Backup-ADATA**, encrypted APFS, primary · **My Passport**, the second
rotation/offsite drive once it's reformatted). Print `tm-health` for live status;
read this when you actually need to get data back.

---

## The mental model (important)

- **Each drive is a complete, independent backup.** You do *not* need both to
  restore. Whichever drive you have in hand can restore everything it holds.
- **Each is encrypted.** You'll be prompted for that drive's password (the one
  saved in your password manager) the first time you mount it. If macOS saved it
  to the keychain it unlocks silently.
- **The offsite drive is only as fresh as its last backup.** If you're restoring
  something from *yesterday* and the offsite drive was last synced two weeks ago,
  use the onsite (more recent) drive. `tm-health` shows each drive's last-backup
  age so you can pick the right one.

---

## 1. Restore a file or folder — the easy way (Finder / Enter Time Machine)

1. Connect the drive you want to restore from. Unlock it if prompted.
2. In Finder, open the folder where the file *used to live* (or any folder).
3. Enter Time Machine:
   - Menu bar → Time Machine icon → **Browse Time Machine Backups**, or
   - System Settings has the backup; the Time Machine "star" menu is fastest.
4. Use the **timeline on the right edge** to step back to a date when the file
   existed. Each tick is a backup. Spotlight/search works inside the window.
5. Select the file or folder → **Restore**. It's copied back to its original
   location (or choose "Restore to…" via right-click for a different spot).

**To restore from a *specific* drive** when both are connected: in the Time
Machine browser, click the Time Machine menu while holding **Option** → **Browse
Other Backup Disks**, and pick the drive.

---

## 2. Restore from the command line (`tmutil`)

Useful for scripted restores, headless work, or when the GUI is cranky.

**List the backups on a mounted drive:**
```sh
tmutil listbackups -d "/Volumes/Backup-ADATA"
```
Each line is a backup snapshot path, e.g.
`/Volumes/Backup-ADATA/<machine>/2026-10-14-094501`.

**Browse one** — the snapshot is a normal filesystem tree; just look inside:
```sh
ls "/Volumes/Backup-ADATA/<machine>/2026-10-14-094501/Macintosh HD - Data/Users/toner/"
```

**Restore a file or directory** (preserves permissions/metadata; `-v` verbose):
```sh
# tmutil restore <source-in-backup> <destination>
tmutil restore -v \
  "/Volumes/Backup-ADATA/<machine>/2026-10-14-094501/Macintosh HD - Data/Users/toner/notes.md" \
  "/Users/toner/notes.md"
```
For a directory, point source at the folder and destination at where it should
land. (A plain `cp -a` from the snapshot works too, but `tmutil restore` keeps
ACLs and extended attributes.)

**Find the latest backup path quickly:**
```sh
tmutil latestbackup        # prints the newest completed backup for this Mac
```

---

## 3. Restore the whole Mac (disaster recovery)

If the Mac is dead or wiped:

1. Boot the replacement/clean Mac. During **Setup Assistant**, choose
   **Migrate from Mac, Time Machine backup, or Startup disk** → *From a Time
   Machine backup*. (Or on a running Mac, open **Migration Assistant**.)
2. Connect a backup drive, unlock it (have the password).
3. Pick the drive, then the backup date, then what to migrate (apps, data,
   users, settings). Let it run.

Use the drive with the **most recent** good backup — check `tm-health` first if
you have both drives.

---

## 4. Good habits / gotchas

- **Test a restore before you need one.** Once a quarter, restore a random file
  from each drive. A backup you've never restored from is a hope, not a backup.
- **Keep the drive passwords in your password manager.** Encrypted backups have
  *no* recovery path if the password is lost.
- **Don't** unmount/eject or `diskutil` a drive mid-backup. Let Time Machine own
  a connected destination.
- **Offsite freshness:** when `tm-health` flags "swap it in," bring the offsite
  drive home, let it run a backup, then rotate it back out.
- **Restores are additive/safe:** restoring an old version doesn't touch your
  other backups — every snapshot is an independent restore point.

---

*Status any time:* `tm-health` · *this guide:* `tm-health restore`
