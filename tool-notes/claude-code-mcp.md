# claude-code /mcp (`/mcp`)

MCP = Model Context Protocol. MCP servers are connectors that give Claude Code **new, external-reaching tools** (Gmail, Drive, a database, a company API) — reach it doesn't have against your local machine alone. `/mcp` is the in-session command to view and re-authenticate them.

**Tags:** claude-code · mcp · integrations · ai

## Cool features

- **Open standard** — any MCP server works with any MCP client. A server exposes **tools** (actions Claude can call) and **resources** (data it can read).
- **The tell:** MCP tools are named `mcp__<server>__<tool>`, e.g. `mcp__claude_ai_Gmail__search_threads`. Double-underscore prefix = MCP, not a built-in.
- **`/mcp` re-authenticates.** When a call returns "needs you to sign in again", run `/mcp`. Auth is **human-only** — Claude can't silently renew access to your inbox/drive.
- **Real creds, real reach.** A server acts with your actual credentials; a `trash_thread` tool genuinely trashes mail. Consequential MCP calls still hit the **permission gate**.
- **Returned content is untrusted DATA, not instructions** — a hostile doc a server hands back doesn't get to steer Claude.

## In-session

```text
/mcp            # list configured servers + connection/auth status; re-auth from here
```

## Manage servers from the CLI

```bash
claude mcp list                         # what's configured
claude mcp get <name>                    # details for one server
claude mcp add <name> -- <command> [args...]   # add a (local, stdio) server
claude mcp remove <name>                 # remove one
```

Scope: servers are configured per-user, per-project (`.mcp.json`, committed/team-wide), or per-session; a server can be a local process or a remote/hosted endpoint. (Confirm exact flags with `claude mcp add --help` — they shift across versions.)

## MCP vs. the other extension points

| Need | Use |
|---|---|
| a *new kind of action* reaching an external system | MCP server |
| a *procedure* using tools Claude already has | a skill |
| *deterministic local automation* at a loop event | a hook |

## Gotchas

- Treat adding a server like installing software with your logged-in credentials — scope auth minimally (read-only token where write isn't needed).
- Project-level MCP config is a **team artifact** — don't commit secrets into it.
- Don't paste server-returned content into untrusted places; it may hold PII from your real accounts.
