# davinci-resolve

DaVinci Resolve 21 — free GUI video editor/colorist (Mac App Store). No CLI; this is the reusable split-screen + color-managed export workflow (wide shot + cropped close-up, exported H.264 .mov).

**Tags:** video · media · gui

## Worth remembering

- **Paste Attributes copies a whole look between clips.** Copy a finished clip, then on another clip Option+V → check **Transform** and **Cropping** → Apply, and the Zoom/Position/Crop all come across. This is how one split-screen layout is reused across many timelines.
- **Color Management auto-converts mixed HDR/SDR.** DaVinci YRGB Color Managed with SDR Rec.709 output correctly converts iPhone HDR (HLG) clips and leaves SDR clips alone — no per-clip grading.
- **Close-ups are cropped from the original clip, not re-filmed.** Filming a screen adds noise, glare, and moiré; a digital crop keeps original quality and stays in sync for free.
- **Fusion macros become reusable title templates** that appear under Effects → Titles in every project.

## One-time setup

### Preferences (DaVinci Resolve → Preferences)

- System → General: check **Use Mac display color profiles for viewers**.
- User → Project Save and Load: turn on **Live Save** (and optionally Project Backups).
- Click **Save** at the bottom right. Some settings need a restart.

### Project Settings (gear icon at bottom right, or File → Project Settings)

- **Master Settings:** timeline resolution 1920×1080; frame rate matched to the footage (set when the first clip is imported — it locks once a timeline exists).
- **Color Management:** Color Science **DaVinci YRGB Color Managed**, output **SDR Rec.709** (Rec.709-A if offered). Converts iPhone HDR (HLG) clips; leaves SDR unchanged.
- **Image Scaling:** Resize filter **Sharper** (helps a zoomed close-up).
- Click **Save**. Closing the window without saving discards the changes.

### Make it the default for new projects

In Project Settings, open the **•••** / gear menu at the top right → **Save As User Default Config** → **Save**. New projects inherit these settings; existing ones aren't affected.

### Render preset (Deliver page)

- Format **QuickTime**, Codec **H.264**, Resolution/Frame rate: Timeline.
- Video tab → **Advanced Settings** (bottom): Color Space Tag **Rec.709**, Gamma Tag **Rec.709-A**.
- Audio tab: **Export Audio** checked, Codec **AAC**, 256 kb/s.
- Save via the **•••** menu at the top right of Render Settings → **Save As New Preset** or **Update Preset**. Render presets apply across all projects.

## The three pages you use

Resolve's pages are the icons along the **bottom row**. For this workflow only three matter, in order:

1. **Media Storage** — import raw videos, name them, trim dead air off the beginnings/endings, create a timeline per video.
2. **Edit** — build the split screen on each timeline.
3. **Deliver** — render each timeline to an .mov.

(Cut, Fusion, Color, and Fairlight also live on that row but aren't part of the normal pass; Fusion is used only once, for the title templates below.)

## Importing footage

- Keep source .MOV files in a permanent folder before importing — Resolve links to files rather than copying them. Moving them later causes "media offline" (fix with right-click → Relink Selected Clips).
- Import on the **Media Storage** page. If Resolve offers to change the project frame rate to match the footage, click **Change** (it locks once a timeline exists).
- **Name each clip** in the Master/Source list, and **trim the dead air** off the beginnings and endings.
- Make **one timeline per video**: right-click **one** clip → **Create New Timeline from Selected Clips**, one clip at a time. Selecting several at once puts them back-to-back on V1 instead of in separate timelines.

## Building the split screen (Edit page)

Pick a timeline (dropdown above the viewer, or double-click in the Media Pool). A new timeline opens with one **V1** video track and one **A1** audio track.

Layout: **V1 = wide shot (left)**, **V2 = zoomed close-up (right)**. V2 covers V1 wherever they overlap, so both are cropped. Duplicating V1 up to V2 gives the second layer. The three settings that make the split render correctly are **Zoom**, **Position X**, and **Cropping** — dialed in per track below.

### 1. Duplicate the clip onto V2

1. Turn off **Linked Selection** (chain-link icon in the timeline toolbar) so the audio isn't duplicated.
2. Hold **Option** before clicking, drag the V1 clip straight up to V2 at the same start point, and release the mouse before releasing Option. Result: same video on V1 and V2, single audio track.
3. If the clip moved instead of copying: with Linked Selection off, Option-drag it back down to V1.

### 2. Open the Inspector

Click **Inspector** at the top right. Click empty timeline space first, then select only one clip — Inspector changes apply to every selected clip.

### 3. V1 — the wide shot (left)

For this layout, Crop Left = Crop Right = c and Position X = −c. V1's visible width = 1920 − 2c.

| Split (V1/V2) | Crop Left | Crop Right | Position X |
|---|---|---|---|
| 50/50 | 480 | 480 | −480 |
| 55/45 | 432 | 432 | −432 |
| ~57/43 | 408 | 408 | −408 |
| 60/40 | 384 | 384 | −384 |

Alternative if the crop cuts off too much of the subject: set Zoom to about 0.5 instead of cropping, so the full frame fits in the left half with black bars above and below.

### 4. V2 — the close-up (right)

1. Transform → **Zoom** 2.0 (2.2 for ~10% tighter). X and Y are linked.
2. Frame the subject in the right half: in the viewer's bottom-left overlay dropdown choose **Transform** and drag the image, or drag the Position X/Y values. Position X is positive. Turn the overlay off afterward.
3. **Crop Left only.** Increase it until the close-up's left edge meets V1's right edge. Crop Right isn't needed — the zoomed image already extends off-screen to the right.
4. Cropping is applied **before** zoom, so V2's crop numbers won't be neat values; judge by eye. Changing the zoom later moves the edge, so re-adjust Crop Left and Position afterward.
5. If the subject drifts out of frame over the clip, add Position keyframes (the diamond next to Position).

Tips:
- To view V1 alone, click the film-strip icon in the V2 track header to hide that track.
- Play the whole timeline through before exporting.

### 5. Reuse the layout on other timelines

1. In the finished timeline, select V1 → **Cmd+C**. Copying the clip grabs all of its track info, including Transform (Zoom, Position X) and Cropping.
2. In the new timeline, select V1 → **Option+V** (Paste Attributes) → check **Transform** and **Cropping** → Apply.
3. Option-drag the new V1 to V2 (Linked Selection off), then paste V2's attributes from the finished timeline the same way.
4. Re-frame V2's Position for that clip.

Switch timelines with the dropdown above the viewer, or by double-clicking a timeline in the Media Pool.

## Header and footer text (Fusion title templates)

Text varies but the style stays the same, so make reusable templates:

1. Add a **Text+** title (Effects → Titles) and style it as the header (top) or footer (bottom).
2. On the **Fusion** page, select the Text+ node → right-click → **Macro → Create Macro**. Check **StyledText** so the text stays editable. Name it and save.
3. Make sure the `.setting` file is in `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Templates/Edit/Titles/`, then restart Resolve. The template then appears under Effects → Titles in every project.
4. Set the text once on the first timeline, then **Duplicate Timeline** for the next videos and swap the clips.

Put titles on tracks above V2 (V3/V4). Template style changes apply only to new uses, not to existing timelines.

For a static overlay that never changes (logo, URL): render it once on the Deliver page as QuickTime **ProRes 4444** with **Export Alpha**, then import it like any other clip.

## Export (Deliver page)

Move to the **Deliver** icon on the bottom row, name the output and pick a location (**Browse**), then **Add to Render Queue** → **Render All**. Detailed steps:

1. Check the timeline name in the dropdown above the viewer.
2. Choose the render preset.
3. **File Name:** the field under Preset (default "Untitled"). Leave off the extension.
4. **Location:** Browse to an export folder kept separate from source footage.
5. Render: **Entire Timeline**.
6. **Add to Render Queue**, then **Render All**. The progress bar appears only after Render All.
7. Open the output in QuickTime and check the seam, framing, and color.

Batch export: queue each timeline (switch timeline, set file name, Add to Render Queue), then Render All once.

Queued jobs keep the settings they had when added. After changing settings, remove the old job (X) and queue it again. When re-rendering over an existing file, allow the overwrite or add a version suffix.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Footage looks darker or grainier than in QuickTime | Usually iPhone HDR interpreted as SDR: use DaVinci YRGB Color Managed with SDR Rec.709 output. Also check the Mac display profile preference. Real noise: add light, use less zoom. |
| Close-up looks bad when filmed from the screen | Don't film the screen. Crop in Resolve instead (see above). |
| Export looks washed out or shifted | Gamma Tag Rec.709-A in the render Advanced Settings. |
| Clip moved to V2 instead of copying | Hold Option before clicking and release it after dropping. Option-drag back down with Linked Selection off. |
| Both clips changed together | Both were selected. Deselect everything, then select one clip. |
| Zoom change made V2 overlap V1 | Crop happens before zoom. Increase V2's Crop Left and re-center Position. |
| No progress bar | The job is only queued. Click Render All. |
| Theme / lighter UI | Resolve 21 doesn't offer UI themes. Use macOS display scaling for readability. |
