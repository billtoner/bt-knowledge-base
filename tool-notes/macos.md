# macOS built-ins

Native desktop utilities I reach for occasionally — screen capture, Markup annotation. No downloads, no BBEdit (it's text-only; it can't draw on an image).

**Tags:** macos · gui

## Annotate a screenshot with a red arrow

Two paths — catch the thumbnail, or edit the saved file later.

```text
# Fastest — the flash thumbnail (bottom-right after any ⌘⇧-capture)
click thumbnail  →  Markup opens  →  Shapes tool → arrow  →  drag tail→head
                    color swatch → red  →  thickness control → bolder  →  Done

# A file already saved to disk — Preview
open in Preview  →  ⇧⌘A (toggle Markup)  →  Shapes → arrow  →  drag
                    border-color swatch → red  →  ⌘S (or File → Export)
```

- Arrow has end-dots to reposition each tip and a middle handle to curve it.
- Same Markup toolbar also does: text box, highlight, blur/redact (Shapes → the pixelate square), crop.

## Screen capture shortcuts

```text
⌘⇧3      whole screen → file on Desktop
⌘⇧4      crosshair: drag a region  (Space toggles window-capture mode)
⌘⇧5      capture toolbar: region/window/full, screen recording, options
⌃ + any  add Control → copies to clipboard instead of saving a file
```

- **⌘⇧5 → Options** sets save location, a capture timer, and whether the thumbnail flashes.
- Default is a `.png` on the Desktop named `Screenshot <date> at <time>.png`.

## Third-party (only if annotating often)

- **CleanShot X** / **Shottr** — capture-and-annotate in one step: nicer arrows, numbered steps, scrolling capture, built-in blur. Worth it only if this is a frequent task; for a one-off red arrow, Markup is enough.
