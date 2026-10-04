# claude-code hooks

Shell commands the Claude Code harness runs automatically at loop events. Deterministic — the harness runs them, not the model, so they can't be forgotten or talked out of (vs. CLAUDE.md, which only *asks*).

**Tags:** claude-code · automation · hooks · ai

## Cool features

- **PreToolUse can BLOCK a call.** Exit 0 = allow, non-zero (convention: exit 2) = deny and hand the reason back to Claude. A real guardrail, not a wish.
- **Events:** `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SessionStart` (and more). The "recent context" at session start is a `SessionStart` hook.
- **Live in settings JSON, not markdown** — the harness reads them, not Claude.
- **Each hook gets JSON on stdin:** `tool_name`, `tool_input.file_path`, `tool_input.command`, etc. Parse with `jq` (or python).
- **`matcher` is a tool-NAME regex** (`Edit|Write`, `Bash`). It does NOT match file paths — filter the path inside the command.
- **Fail open.** On any internal error, exit 0 so the normal permission prompt still gates the call.

## Where they live (scope, like CLAUDE.md)

```
~/.claude/settings.json              # you, all projects
<repo>/.claude/settings.json         # project, committed (team-wide)
<repo>/.claude/settings.local.json   # project, just you (gitignored)
```

## settings.json shape

```jsonc
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",                     // tool-name regex
        "hooks": [
          { "type": "command", "command": "/Users/me/.claude/hooks/fmt.sh" }
        ]
      }
    ]
  }
}
```

Validate after editing: `jq empty ~/.claude/settings.json && echo ok`.

## Reading the payload inside a hook

```bash
#!/usr/bin/env bash
set -uo pipefail
input=$(cat)                                                   # JSON on stdin
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // ""')
cmd=$(printf '%s'  "$input" | jq -r '.tool_input.command  // ""')
case "$path" in
  *.tf) terraform fmt "$path" ;;                                # act on the edited file
esac
exit 0                                                          # PostToolUse can't block anyway
```

## Hook vs. the softer layers

| Want | Use |
|---|---|
| "please usually do X" | CLAUDE.md (soft request) |
| "a procedure Claude follows when relevant" | a skill |
| "X runs every time, guaranteed, at event E" | a hook |

## Gotchas

- Over-broad `PreToolUse` matcher + a non-zero exit can wedge the session ("everything denied"). Scope matchers tightly, test the command standalone first.
- Hooks run on the critical path of the loop — keep them fast.
- A hook runs arbitrary shell automatically; a bad one can loop or wreck a workflow.
