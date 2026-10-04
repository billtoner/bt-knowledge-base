# claude-code subagents

Delegate a task to a *separate* Claude instance with its own context window. It works independently and returns the **result**, not the exploration it waded through.

**Tags:** claude-code · ai · agents

## Cool features

- **Two payoffs:** context isolation (the 40 files it reads land in ITS window, not yours) + parallelism (launch several, they run concurrently).
- **Defined as markdown** in `~/.claude/agents/<name>.md` (user) or `<repo>/.claude/agents/<name>.md` (project), with frontmatter.
- **`model:` pins which model it runs** — aliases `sonnet` / `opus` / `haiku` / `fable`, a full id, or `inherit`. This is how you run a task on a non-default model.
- **A skill can run in a subagent** via SKILL.md frontmatter `context: fork` + `agent: <name>` — that's how you pin a skill to a model (SKILL.md itself has no `model:` field).
- **Fork** inherits the current conversation context; a fresh general agent starts clean.
- **Permission gate still applies** inside a subagent.

## Agent definition

```markdown
---
name: sweep-runner
description: Runs the code-sweep procedure on Fable. Invoked by the sweep skill.
model: fable
tools: Read, Grep, Glob, Bash, Write, Agent    # Agent = allowed to spawn further subagents
---
Instructions the subagent follows go here (its system prompt).
```

Model resolution order: per-invocation override → agent's `model:` → `CLAUDE_CODE_SUBAGENT_MODEL` env → main conversation's model.

## When to delegate vs. stay inline

| Delegate (subagent) | Stay inline |
|---|---|
| broad fan-out search over many files | small, single-file edit |
| independent chunks that run at once | steps that depend on each other |
| want a specialized lens (planner, explorer) | you need all the raw detail anyway |

Decider: *would delegating keep my context clean (big search) or cost me the detail I need (small edit)?*

## Built-in agent types

- `Explore` — read-only fan-out search (see [claude-code-explore](claude-code-explore.md)).
- `Plan` — architect; designs an implementation plan, makes no edits.
- `general-purpose` — broad tools, researches/executes multi-step tasks.
- plus any you define in `.claude/agents/`.

## Gotchas

- **Don't overspawn** — five agents for a one-agent job burns tokens and wall-clock. Match fan-out to the work.
- A subagent returns a **summary**; if you needed the raw detail, ask for it or do it inline.
- Subagents can't ask you questions mid-task — give a complete brief up front.
