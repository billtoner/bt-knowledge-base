# TODO

Backlog for the next week or so. Check items off as they land; move finished
ones to Done with the date.

## Backlog

### Re-bucket to a durable, function-first taxonomy

Agreed 2026-06-16 (comprehensive option). Replace the current 16 categories
(notably the 23-tool `Network` blob, the vendor bucket `AWS CLI`, and the
`Useful Tools` junk drawer) with function-first buckets that have room to grow.

**Prerequisite (do first):**
- [ ] `kb move <tool> <category>` — recategorize a tool safely (update category
  files + index, remove an emptied category + unlink it). Migrate through this,
  not by hand.

**Open decision before migrating:**
- [ ] Category-name casing: keep original casing hyphenated (`Network-Diagnostics`,
  `AWS-CLI`) or fully lowercase to match file slugs (`network-diagnostics`)?
  (Supersedes the earlier "names to be `-`-separated" item.)

**Target taxonomy** (current tools → bucket; "—" = new/placeholder):
- Version Control ← git, delta, lazygit, tig
- Languages & Scripting ← python/js/perl one-liners, bash-idioms
- Markup & Docs ← html-snippets, grip
- Build & Packaging ← — (make, uv, npm, cargo, brew)
- Search ← ripgrep, fd
- Text & Data Processing ← jq, yq, jc, gron, sort, vd
- Databases ← sqlite3, sqlite-utils, db-browser-for-sqlite
- Files & Directories ← bat, eza, rsync
- Shell & Terminal ← atuin, zoxide
- System & Services ← systemctl, journalctl
- Performance & Profiling ← watch, py-spy, viztracer, aiomonitor
- Hardware & Devices ← lsusb, bluetoothctl, hcitool, pactl
- Remote Access ← ssh, scp, ssh-add
- HTTP & API Clients ← curl, httpie, wget
- Network Diagnostics ← dig, host, whois, ss, nmap, mtr, traceroute, tcpdump, ngrep, iperf3, iftop, nethogs
- Network Config & Firewall ← ip, nmcli, iw, ifconfig, iwconfig, iptables, nft, ufw, wg
- Cloud CLIs ← nosql-workbench (aws, gcloud, az)
- Containers & Orchestration ← — (docker, kubectl, helm, compose)
- Infrastructure as Code ← ansible (terraform, pulumi)
- Security & Secrets ← — (gpg, openssl, age, vault)

## Done
