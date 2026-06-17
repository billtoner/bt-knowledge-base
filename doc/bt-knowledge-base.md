# Command Line commands

A categorized index of CLI tools I want to refresh on. Click into a category for its tools; each tool links to a note with examples. Empty categories below are placeholders waiting for content.

## Find a tool

Run from the repo root:

```bash
# 1. Open a tool note by exact name (tab-completion works)
bat tool-notes/<name>.md                 # e.g. bat tool-notes/nmcli.md

# 2. Search all tool notes by keyword (matches inside the files)
rg -li <keyword> tool-notes/             # files that mention <keyword>
rg <keyword> tool-notes/                 # with surrounding lines

# 3. Fuzzy-find and open (requires fzf)
fd . tool-notes/ -e md | fzf --preview 'bat --color=always {}' | xargs -r $EDITOR

# 4. List every tool currently documented
fd . tool-notes/ -e md -x basename {} .md
```

Shell function (optional — add to `~/.zshrc` for `tool <name>`):

```bash
tool() {
    local repo="$HOME/Documents/repos/bt-knowledge-base"
    if [[ -z "$1" ]]; then
        fd . "$repo/tool-notes" -e md | fzf --preview "bat --color=always {}" | xargs -r ${EDITOR:-bat}
    else
        ${EDITOR:-bat} "$repo/tool-notes/$1.md"
    fi
}
```

## Categories

- Archiving
- [Cloud CLIs](categories/cloud-clis.md)
- Containers & Orchestration
- [Databases](categories/databases.md)
- Disk
- [Files & Directories](categories/files-directories.md)
- [Hardware & Devices](categories/hardware-devices.md)
- [HTTP & API Clients](categories/http-api-clients.md)
- [Infrastructure as Code](categories/infrastructure-as-code.md)
- Installing packages
- [Languages & Scripting](categories/languages-scripting.md)
- [Markup & Docs](categories/markup-docs.md)
- [Network Config & Firewall](categories/network-config-firewall.md)
- [Network Diagnostics](categories/network-diagnostics.md)
- [Performance & Profiling](categories/performance-profiling.md)
- [Remote Access](categories/remote-access.md)
- [Search](categories/search.md)
- Security & Secrets
- [Shell & Terminal](categories/shell-terminal.md)
- [System & Services](categories/system-services.md)
- [Text & Data Processing](categories/text-data-processing.md)
- [Version Control](categories/version-control.md)
