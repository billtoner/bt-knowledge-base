# viztracer

Trace-based profiler with a beautiful interactive web viewer. Strength: visualizing **async
execution** and per-function timing across many threads/coroutines.

**Tags:** profiling · python

## Status for FPOC

**Defer unless** you have a specific async timing mystery. Heavier ceremony than py-spy:
you wrap a function call (or run a process under viztracer), it dumps a JSON trace, you
open it in a browser viewer. Not "attach to running process" like py-spy.

## How it works

Unlike py-spy (sampling), viztracer **records every function entry and exit** to disk.
Output is a JSON trace file you open in a browser (vizviewer ships with the package).

You get a perfetto-like timeline:
- Horizontal axis = time
- Vertical lanes = threads / asyncio tasks
- Bars = function calls (width = duration)
- Click to zoom in to ns-level detail

## Basic usage

### From a Python script

```python
from viztracer import VizTracer

with VizTracer(output_file="trace.json"):
    do_the_thing()
```

### From the command line (wraps an entire script)

```bash
viztracer my_script.py
vizviewer trace.json   # opens browser viewer
```

### With pytest

```bash
viztracer --include_files audiopulse -- pytest tests/unit/test_score.py
vizviewer trace.json
```

## Why it's good for async code

`py-spy` shows you which Python function used the most CPU. But asyncio code spends most
of its time *awaiting* — sleeping, waiting on I/O, parked in `await`. A sampling profiler
misses that detail.

viztracer instruments every `await` point. The timeline shows precisely:
- When each coroutine started
- When it suspended at an `await`
- When it resumed
- Which coroutines blocked others

This is what you'd want if you suspected "the BLE consumer is blocking the audio coroutine
for X ms periodically" but couldn't see it from regular logging.

## When to reach for viztracer over py-spy

| Need | Tool |
|---|---|
| "Where is wall-clock time going?" — running process | py-spy |
| "Why is this async pipeline sometimes slow?" | viztracer |
| "Show me the actual order of async events" | viztracer |
| Pre-deployment "is anything obviously wrong" sweep | py-spy |
| Debugging a specific test that times out | viztracer |
| Long-running production process | py-spy |

## Install

```bash
uv pip install viztracer    # into FPOC's .venv
# OR system-wide:
uv tool install viztracer
```

## Useful flags

- `--include_files audiopulse` — only instrument FPOC code (skip stdlib, bleak, etc.)
- `--exclude_files tests` — skip test scaffolding
- `--max_stack_depth 30` — limit recursion drilling
- `--ignore_c_function` — don't trace C extensions (smaller traces)
- `--log_async` — explicit async event labeling
- `--minimize_memory` — for long traces (>10s)

## Cost

Traces are LARGE for long runs (megabytes per second). Run for 10–60s targeted at the specific
window where the bug appears, not "all day."
