# starship

Fast, cross-shell prompt configured from a single `~/.config/starship.toml`. Beyond looks, it has real introspection commands and per-project prompts.

**Tags:** shell · prompt

## Cool features

- **`starship timings`** — per-module render time; the go-to when the prompt feels laggy (usually a git or cloud module hitting the network).
- **`starship explain`** — explains every module currently in your prompt ("what is that symbol?").
- **Presets** — `starship preset --list` then apply one to a file; fastest way to a good-looking prompt.
- **Per-project prompt** — point `$STARSHIP_CONFIG` at a repo-local `.starship.toml`.
- **Custom modules** — run any command and render its output conditionally (`when = ...`).

## Introspection / debugging your prompt

```bash
starship explain            # explains every module currently in your prompt
starship timings            # per-module render time — find what's slowing the prompt
starship module directory   # render a single module standalone (debugging)
starship config             # open the config in $EDITOR
starship print-config       # dump the effective config (defaults + overrides)
```

## Presets (fastest way to a good-looking prompt)

```bash
starship preset --list
starship preset nerd-font-symbols -o ~/.config/starship.toml
starship preset pastel-powerline -o ~/.config/starship.toml
```

## Per-project prompt

```bash
export STARSHIP_CONFIG="$PWD/.starship.toml"   # in a project shell, point at a repo-local config
```

## Setup (shell rc — keep LAST)

```bash
eval "$(starship init zsh)"     # goes at the very end so nothing overrides it
eval "$(starship init bash)"
```

## Useful config snippets (`~/.config/starship.toml`)

```toml
# Don't let a slow module hang the prompt
command_timeout = 500
add_newline = true

# Show how long the last command took (only if slow)
[cmd_duration]
min_time = 1000
format = "took [$duration](bold yellow) "

# Python venv + version, only in Python projects
[python]
format = '[${symbol}${version}( \($virtualenv\))]($style) '

# Git status: ahead/behind/stashed/conflicts at a glance
[git_status]
ahead = "⇡${count}"
behind = "⇣${count}"
diverged = "⇕⇡${ahead_count}⇣${behind_count}"
stashed = "*${count}"

# Background jobs indicator
[jobs]
symbol = "✦"
number_threshold = 1

# AWS profile/region (handy when you juggle accounts)
[aws]
format = 'on [$symbol($profile )(\($region\) )]($style)'

# A custom module: current k8s namespace, only when kubectl config exists
[custom.k8s]
command = "kubectl config view --minify -o jsonpath='{..namespace}' 2>/dev/null"
when = "command -v kubectl"
format = "[⎈ $output]($style) "
```

## Right-hand prompt (zsh/fish/newer shells)

```toml
right_format = "$time"          # push time to the right side
[time]
disabled = false
format = "[$time]($style)"
```
