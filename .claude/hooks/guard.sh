#!/usr/bin/env bash
# .claude/hooks/guard.sh
# PreToolUse hook. Fires on Bash, Read, Edit, Write, NotebookEdit.
#
# Priority order:
#   1. Sensitive-path access (any tool, any method)  -> deny
#   2. Destructive / network / escalation Bash        -> deny
#   3. Known read-only command (no shell metachars)   -> allow
#   else: stay silent (exit 0) and defer to settings.json / normal prompt.
#
# Parsing uses python3 (no jq dependency). exit 1 is never used because it
# fails OPEN; on any internal error we exit 0 so the normal permission
# prompt still gates the call.

set -uo pipefail

SENSITIVE='(\.env($|[^a-zA-Z])|\.env\.|/\.aws/|aws/credentials|\.ssh/|id_rsa|id_ed25519|\.pem($|[^a-zA-Z])|secrets?/|credentials|\.netrc|\.pgpass|terraform\.tfstate|\.git/config)'
DANGER='(\brm\b|\bsudo\b|\bdd\b|\bmkfs\b|\bcurl\b|\bwget\b|\bnc\b|\bssh\b|\bscp\b|\bchmod\b|\bchown\b|\bgit\s+push\b|\bgit\s+reset\b|\bgit\s+clean\b|\baws\s+s3\s+rm\b|>\s*/|\btruncate\b|\bshred\b)'
SAFE_CMDS='^(cd|ls|cat|grep|rg|find|head|tail|wc|awk|sed|pwd|echo|which|whereis|stat|file|tree|less|more|sort|uniq|diff|cut|tr|jq|date|env|printenv|whoami|hostname|uname|df|du|ps|top|vcgencmd|systemctl status|journalctl|git status|git log|git diff|git show|git branch)\b'

PY=$(command -v python3 || command -v python || true)
if [ -z "$PY" ]; then
  echo "guard.sh: python not found; hook inactive" >&2
  exit 0
fi

input=$(cat)

read -r tool path cmd < <(
  printf '%s' "$input" | "$PY" -c '
import sys, json, base64
try:
    d = json.load(sys.stdin)
except Exception:
    print(""); sys.exit(0)
ti = d.get("tool_input") or {}
tool = d.get("tool_name") or ""
path = ti.get("file_path") or ti.get("notebook_path") or ""
cmd  = ti.get("command") or ""
def enc(s): return base64.b64encode(s.encode()).decode() or "-"
print(tool, enc(path), enc(cmd))
' 2>/dev/null
)
[ -z "${tool:-}" ] && exit 0

dec() { [ "$1" = "-" ] && echo "" || printf '%s' "$1" | base64 -d 2>/dev/null; }
path=$(dec "${path:-}")
cmd=$(dec "${cmd:-}")

deny() {
  reason=$("$PY" -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$1")
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":%s}}\n' "$reason"
  exit 0
}
allow() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}\n'
  exit 0
}

case "$tool" in
  Read|Edit|Write|NotebookEdit)
    if printf '%s' "$path" | grep -Eiq "$SENSITIVE"; then
      deny "Blocked by policy: '$path' is a protected/sensitive path (credentials, keys, secrets). Refused."
    fi
    exit 0
    ;;
  Bash)
    [ -z "$cmd" ] && exit 0
    if printf '%s' "$cmd" | grep -Eiq "$SENSITIVE"; then
      deny "Blocked by policy: command references a protected/sensitive path. Refused."
    fi
    if printf '%s' "$cmd" | grep -Eq "$DANGER"; then
      deny "Blocked by policy: destructive/network/escalation command. User must run manually if intended."
    fi
    if printf '%s' "$cmd" | grep -Eq '[|;&]|\$\(|`|>|<'; then
      exit 0
    fi
    if printf '%s' "$cmd" | grep -Eq "$SAFE_CMDS"; then
      allow
    fi
    exit 0
    ;;
  *)
    exit 0
    ;;
esac
