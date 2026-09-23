# pactl

Control PulseAudio (and PipeWire, via its pulse-compatibility layer) from the command line. List sinks/sources, switch default output, set volume, load modules, watch events.

**Tags:** hardware · audio

## Cool features

- **`@DEFAULT_SINK@` / `@DEFAULT_SOURCE@`** — symbolic names that always resolve to whatever is currently default, so scripts don't break when the device changes.
- **Relative volume changes.** `+5%` / `-5%` adjust from current, no need to read-modify-write.
- **`subscribe`** streams every server event live — great for figuring out which events fire when you plug headphones in.
- **Card profiles switch in one command.** `set-card-profile` flips HDMI / Analog / A2DP / headset modes.
- **Move running streams between outputs.** `move-sink-input <id> <sink>` reroutes an already-playing app without restarting it.
- **Works against PipeWire too.** On PipeWire systems with `pipewire-pulse`, all of these still work.

## Server / device inventory

```bash
pactl info                                          # server, default sink/source, sample format
pactl list sinks short                              # output devices, one per line
pactl list sources short                            # input devices, one per line
pactl list cards short                              # sound cards
pactl list sink-inputs                              # what apps are currently playing
pactl list source-outputs                           # what apps are currently recording
```

## Switch default output / input

```bash
pactl set-default-sink   alsa_output.pci-0000_00_1f.3.analog-stereo
pactl set-default-source alsa_input.usb-Blue_Microphones_Yeti.analog-stereo
```

## Volume

```bash
pactl set-sink-volume @DEFAULT_SINK@ 50%            # absolute
pactl set-sink-volume @DEFAULT_SINK@ +5%            # bump up
pactl set-sink-volume @DEFAULT_SINK@ -5%            # bump down
pactl set-sink-mute   @DEFAULT_SINK@ toggle
pactl set-source-volume @DEFAULT_SOURCE@ 80%        # mic
pactl set-source-mute   @DEFAULT_SOURCE@ toggle
```

## Move a running stream

```bash
pactl list sink-inputs short                        # find the sink-input ID
pactl move-sink-input 42 alsa_output.usb-Headphones.analog-stereo
```

## Card profiles (HDMI / A2DP / headset)

```bash
pactl list cards short                              # find card name
pactl list cards | grep -A1 "Profiles:"             # available profiles
pactl set-card-profile bluez_card.AA_BB_CC_DD_EE_FF a2dp-sink    # headphones high-quality
pactl set-card-profile bluez_card.AA_BB_CC_DD_EE_FF headset-head-unit   # headset (mic enabled, lower quality)
```

## Modules

```bash
pactl load-module module-loopback latency_msec=20 source=$MIC sink=$SPEAKER
pactl list modules short
pactl unload-module 27                              # by ID from list
```

## Watch events live

```bash
pactl subscribe                                     # streams events as they happen
pactl subscribe | grep -E "sink|source"             # filter to device events
```

## Killer subcommands

- `info` — server overview
- `list <type> [short]` — `sinks`, `sources`, `cards`, `sink-inputs`, `source-outputs`, `modules`, `clients`, `samples`
- `set-default-sink` / `set-default-source` — switch default device
- `set-sink-volume` / `set-source-volume` — accepts `%`, `+%`, `-%`
- `set-sink-mute` / `set-source-mute` — accepts `1`, `0`, `toggle`
- `move-sink-input <id> <sink>` — reroute a running stream
- `set-card-profile` — flip HDMI/A2DP/headset modes
- `load-module` / `unload-module` — dynamic module management
- `subscribe` — live event stream
