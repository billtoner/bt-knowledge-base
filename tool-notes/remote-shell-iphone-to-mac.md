# remote-shell-iphone-to-mac

SSH into the MacBook from an iPhone — same-Wi-Fi or from anywhere via Tailscale.

**Tags:** remote · ssh · macos · vpn

For when you're away from the Mac but have your phone and need a shell (run `kb`, `pass`, etc.).

## Mac side (once)

- System Settings → General → Sharing → **Remote Login = On** (starts sshd; the panel shows
  the exact `ssh you@host` to use). CLI: `sudo systemsetup -setremotelogin on`.
- Find your address:
  - `whoami` — the SSH username
  - `scutil --get LocalHostName` — Bonjour name → connect as `<name>.local`
  - `ipconfig getifaddr en0` — Wi-Fi IP

## iPhone side

- SSH client app: **Blink Shell** (supports Mosh — survives flaky cell/sleep; top pick) or **Termius**.
- **Same Wi-Fi:** `ssh you@<name>.local` (or the IP).
- **From anywhere:** install **Tailscale** on both devices (same account) → `ssh you@<mac-tailscale-name>`.
  Encrypted mesh VPN, no port-forwarding. The right "from the road" answer.

## Security

- Use **SSH keys**, not passwords: the app generates a keypair (stored in the Secure Enclave),
  add its public key to the Mac's `~/.ssh/authorized_keys`, then disable password login.

## Gotchas

- **MacBook must be awake to answer** — closed lid sleeps → unreachable. Keep it plugged/awake
  or run `caffeinate -s`. No reliable remote wake over Wi-Fi.
- **`pass` over SSH**: `pinentry-mac` is a GUI dialog that won't appear in a headless SSH
  session, so `pass show` hangs. For remote use, add a terminal fallback — `export GPG_TTY=$(tty)`
  and have gpg-agent use `pinentry-curses` so the passphrase prompt shows in the phone's terminal.
