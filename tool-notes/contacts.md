# contacts

Custom CLI (`~/bin/contacts`) to search, export, and round-trip edit macOS Contacts.

**Tags:** macos · contacts · cli

## Cool features

- **Reads the Contacts SQLite stores directly** (all AddressBook sources, merged + de-duplicated) — fast, no Contacts.app launch. Writes go through AppleScript so they sync to iCloud; it never edits the `.abcddb` (that would desync/corrupt).
- **Round-trip editing**: `dump` to JSON, edit, `apply` back. Keyed on each contact's stable id (`<UUID>:ABPerson`), so apply updates in place and never makes duplicates.
- **Digit-normalized phone search** — `contacts 4155551234` matches `+1 (415) 555-1234` regardless of formatting.
- **apply is dry-run by default** (prints a diff), needs `--apply` to write, and takes a timestamped backup to `~/.local/state/contacts/` before any change.
- **Present-only edits**: delete a key in the JSON to leave that field untouched; empty value clears it; emails/phones are replaced as a set from the JSON.

## Search

```bash
contacts smith                 # substring across name/org/email/phone (default command)
contacts 415                   # partial phone / area code
contacts 4155551234            # digits-only; ignores phone formatting
contacts @gmail.com            # by email domain
contacts acme corp             # multi-word = one phrase
contacts --help                # usage
```

## Dump to JSON

```bash
contacts dump                        # all contacts -> stdout (JSON)
contacts dump smith                  # only matches
contacts dump smith -o ~/smith.json  # write to a file
```

JSON per contact: `id`, `first`, `last`, `nickname`, `organization`, `emails[{label,value}]`, `phones[{label,value}]`.

## Edit and apply (round-trip)

```bash
contacts dump "my name" -o ~/me.json   # 1. export one contact
# 2. edit values in ~/me.json (keep its id to update in place)
contacts apply ~/me.json               # 3. DRY RUN: shows diff + "id match: N/N"
contacts apply ~/me.json --apply       # 4. write (backs up current state first)
```

The dry-run's `id match: N/N` line confirms the round-trip key resolves before any write. An id that doesn't resolve is **skipped and reported**, never re-added as a duplicate.

## Permissions (the usual gotchas)

- **Search/dump** read the SQLite store → the terminal needs **Full Disk Access** (System Settings > Privacy & Security > Full Disk Access). Blocked = a clear message, not a crash.
- **apply** drives Contacts.app via `osascript` → first run prompts for **Automation / Contacts** access; approve it. In a non-interactive shell that prompt silently blocks.

## Killer flags

- `dump -o <file>` — write JSON to a file instead of stdout
- `apply --apply` — actually write (default is a dry-run diff)
- `apply --create` — intended to add new (id-less) entries; **not implemented yet** (reports and skips)
