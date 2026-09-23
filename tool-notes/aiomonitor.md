# aiomonitor

Telnet console into a running asyncio event loop. Inspect tasks, stacks, and coroutine state
in a live process. Requires a small **code change** to enable.

**Tags:** profiling · python

## Status for FPOC

**Defer until you have a specific async bug to chase.** Unlike py-spy (drop-in, profile any
process) or viztracer (one-shot trace), aiomonitor needs you to wire it into your service
startup. Cost: ~3 lines of code. Benefit: interactive inspection of running asyncio tasks.

## What it gives you

When wired in, your asyncio service opens a TCP port (default 50101) you can `telnet` into.
Inside the console:

- `ps` — list all running tasks, with their coroutine names and states
- `where <task_id>` — full stack trace of a specific task
- `cancel <task_id>` — cancel a task interactively
- `signal SIGUSR1` — send a signal
- `console` — drop into a live Python REPL inside the event loop

The killer use: **"why is this coroutine hanging?"** You connect, `ps`, find the task that's
been alive for 5 minutes when it should be 50ms, `where` it, see the stack frame, fix it.

## Wiring it in (the cost)

In whatever module owns your asyncio loop startup:

```python
import aiomonitor

async def main():
    loop = asyncio.get_running_loop()
    with aiomonitor.start_monitor(loop=loop):
        await run_forever()
```

That's it. The `with` block starts the telnet listener; everything else stays the same.

## Connecting

```bash
telnet localhost 50101
# Or, more pleasantly:
nc localhost 50101
```

Once connected:

```
asyncio> ps
Task ID   State    Task
1         RUNNING  <Task pending name='main'>
2         RUNNING  <Task pending name='consumer' coro=<consume() done at...>>
...

asyncio> where 2
Stack for <Task pending name='consumer'> (most recent call last):
  File "audiopulse/ble/QueueHandler.py", line 432, in consume
    msg = await self.insole_message_queue.get()
  ...
```

## Useful in FPOC if you ever need it

Concrete cases this would help with:

- **"The BLE consumer task is alive but not draining the queue."** Connect, `ps`, find the
  consumer task, `where` it, see it's blocked at `audio_manager.play_alert` instead of `queue.get`.
- **"AlertHandler stops firing after 30 min."** Connect, see all alert-related tasks,
  inspect their state.
- **"Settings watcher isn't reloading."** Same pattern — find the task, look at its current await.

For your current FPOC issues (audio chain, BLE coexistence, hardware-side problems), aiomonitor
wouldn't help. Save it for the day you suspect an *async-internal* bug.

## Security note

The default port (50101) listens on **127.0.0.1** only, so no remote access. But if you
ever expose it (don't), anyone who connects gets a Python REPL inside your live service —
effectively full code execution. Keep it localhost-only or wrap it in firewall rules.

## Install

```bash
uv pip install aiomonitor
```

## When NOT to use aiomonitor

- Production process you don't want to add a TCP listener to
- Any service where the cost of "occasionally pause loop to handle a telnet command" isn't acceptable
- Anything that isn't asyncio (it's only for asyncio)
- Bugs you can reproduce in a debugger — `pdb` / `breakpoint()` is more direct
