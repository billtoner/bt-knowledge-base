# atuin

Replaces zsh's Ctrl-R with a TUI fuzzy-search backed by SQLite. Stores rich metadata per command.

## Cool features

- **TUI fuzzy search on Ctrl-R** — type to filter, scroll, Enter to run, Tab to edit before running.
- **Rich metadata** — every command stored with: cwd, hostname, exit code, duration, timestamp, session ID.
- **Filter modes** — press Ctrl-R repeatedly inside the TUI to cycle:
    - **Global** (default) — all history, all dirs
    - **Host** — this machine only (relevant if synced)
    - **Session** — only this terminal tab
    - **Directory** — only commands ever run in the current `cwd` ← killer
- **SQLite-backed** at `~/.local/share/atuin/history.db` — durable, queryable.
- **Optional sync** — cross-machine history via atuin.sh or self-hosted server.
- **Stats.** `atuin stats` shows top commands, most-used aliases, etc.

## First-time setup gotcha

Atuin only stores commands typed *after install*. Run this once:

```bash
atuin import zsh
```

Sucks in your existing `~/.zsh_history`. Now Ctrl-R sees your archive.

## Daily commands beyond Ctrl-R

```bash
atuin history list | tail -20                    # last 20 commands
atuin search 'brew install'                      # search from CLI (no TUI)
atuin search --filter-mode directory 'just'      # commands in current dir
atuin stats                                       # fun stats
atuin update                                      # update atuin itself
```

## Privacy escape hatch

- **Leading space prefix** — any command typed with a leading space is NOT saved
  (relies on `setopt hist_ignore_space` in zsh, which atuin respects).
- **`history_filter` in config** — regex list of commands to never store. Useful for credential exports:

```toml
# ~/.config/atuin/config.toml
history_filter = [
    "^export.*TOKEN",
    "^export.*KEY",
    "^export.*SECRET",
    "^export.*PASSWORD",
]
```

## What atuin DOESN'T replace

- **Up-arrow** still uses zsh's native history (per-session). Atuin only binds Ctrl-R.
  Up-arrow = "last thing I ran"; Ctrl-R = "any command I've ever run, fuzzy-searchable."
- To make up-arrow also use atuin: `filter_mode_shell_up_key_binding = "session"` in config.

## Useful in FPOC

```bash
# Directory mode is the win. Try:
cd ~/Documents/repos/FPOC
Ctrl-R Ctrl-R Ctrl-R Ctrl-R   # cycle to [Directory] mode
# Now you see only FPOC commands. Type 'pyright', 'pytest', 'bump', etc.

# Cross-session reach
# That brew install you did 6 weeks ago in a now-closed tab? Ctrl-R + type the package name.

# Audit your own habits
atuin stats    # what do you actually run all day?
```

## Sync

Set up on the default server `https://api.atuin.sh` (end-to-end encrypted — the server stores only ciphertext). Auto-syncs every 5m; `auto_sync = true` is the default.

```bash
atuin register -u <username> -e <email> -p <password>   # first machine only; auto-logs-in
atuin sync                                               # push/pull now (usually automatic)
atuin status                                             # who am I, which server, last sync
```

`atuin key` prints the encryption key — run it in a **plain terminal**, never a logged/shared session, and stash it (+ the password) in the "Atuin Sync" entry in Apple Passwords (iCloud), with the key in the entry's Notes field.

## Restore on a new Mac

The password gets you into the account; the **key decrypts the history**. Both are required:

```bash
atuin login -u <username> -p <password> -k '<encryption-key>'   # -k is MANDATORY
atuin sync                                                       # pulls history down
```

Lose the key and the synced history is undecryptable ciphertext — atuin can't recover it. Creds + key live in Apple Passwords / iCloud ("Atuin Sync", key in Notes); also referenced in `~/dotfiles/MAC-BOOTSTRAP.md`.
