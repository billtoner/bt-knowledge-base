# claude-code Explore agent

Built-in **read-only** fan-out search subagent. Sweeps many files, directories, and naming conventions and returns the conclusion — not the file dumps. Keeps big searches out of your main context window.

**Tags:** claude-code · ai · agents · search

## Cool features

- **Read-only.** It *locates* code; it doesn't edit, review, or audit it. (All tools except the editing/agent-spawning ones.)
- **Context isolation.** The files it reads stay in its window; you get back a tidy list. Use it instead of running a wide `rg`/`grep` inline when you don't need to keep the matches.
- **Breadth is a dial.** Tell it how hard to look: `"medium"` for moderate exploration, `"very thorough"` for multiple locations and naming conventions.
- **Reads excerpts, not whole files** — fast and cheap for "where does X live" questions.

## Good for

```text
"Find every file that calls the ASC API across the repo and list them."
"Which lessons reference the /sweep skill, and where?"
"Where is retry/backoff configured anywhere in this service?"
```

## When NOT to use it

- You need to *change* code (Explore can't edit) → use the main agent or a different subagent.
- The task is a small, known, single-file lookup → just read it inline; a subagent adds overhead and hands back only a summary.
- You need a design/plan rather than locations → use the `Plan` agent instead.

See [claude-code-subagents](claude-code-subagents.md) for the general delegation model.
