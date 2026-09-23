# py-spy

Sampling profiler for Python that attaches to an **already-running process** via `ptrace`.
No code changes, no restart. The killer feature is "the BLE service is doing something weird —
let's see what" without redeploying.

**Tags:** profiling · python

## Status for FPOC

**Probably not needed yet.** FPOC's pain points are at the audio/BT layer, not Python CPU.
Keep this card as a reference for the day Python CPU becomes suspect.

Specifically, py-spy would earn its keep if any of these happened:
- BLE service is using 50%+ CPU on the Pi (currently it sips)
- Session start takes >1s when it should be <100ms
- Dashboard becomes sluggish
- You're about to scale from 3 → 20 participants and want a pre-flight CPU audit

## Three modes

### 1. Live top — interactive

```bash
sudo py-spy top --pid $(pgrep -f 'audiopulse ble' | head -1)
```

Like `top` but per-function. Shows where Python is spending time *right now*, updating live.
`Ctrl-C` to exit. Doesn't touch the process.

### 2. Record to flame graph (SVG)

```bash
sudo py-spy record -d 30 -o /tmp/ble-profile.svg \
    --pid $(pgrep -f 'audiopulse ble' | head -1)

# Then from Mac:
scp pi@audiopulse-2:/tmp/ble-profile.svg ~/Desktop/
open ~/Desktop/ble-profile.svg   # opens in browser, interactive
```

`-d 30` = sample for 30 seconds, write SVG flame graph. The visualization is a hierarchical
"wider = more time spent" view. Click any block to zoom in.

### 3. One-shot thread dump

```bash
sudo py-spy dump --pid $(pgrep -f 'audiopulse webserver' | head -1)
```

Prints the current Python stack of every thread. Useful when a process is hung — see exactly
where each thread is parked.

## Why sudo

`py-spy` uses `ptrace` to read another process's memory. systemd services run as root, so
attaching needs root. On macOS, py-spy also needs to be run as sudo for similar reasons.

## Install on the Pi

```bash
/home/pi/.local/bin/uv tool install py-spy
export PATH="$HOME/.local/bin:$PATH"
py-spy --version
```

## Install on the Mac (if you want to profile local Python)

```bash
uv tool install py-spy
# OR
brew install py-spy
```

## Anti-features (what it isn't)

- Not a debugger — can't set breakpoints or inspect variables.
- Not real-time line-by-line — samples at intervals (default 100Hz), so very fast functions may not appear.
- Not for async-specific introspection — see `viztracer` or `aiomonitor` for that.
- Doesn't show memory — use `memray` if you suspect a memory leak.

## When to reach for py-spy specifically

- "Where is wall-clock time going inside this Python process?"
- "Is X function actually a bottleneck or am I imagining it?"
- "Pre-clinical-deployment sanity check: anything in the hot path I should worry about?"
