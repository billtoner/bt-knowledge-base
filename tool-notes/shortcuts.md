# shortcuts (`shortcuts`)

A dashhub launcher card that beats Chrome's 10-shortcut cap — a grouped HTML grid of link tiles, opened in the browser. Tiles are private monograms (first letter, color hashed from the name) or an emoji you set; no favicons are fetched, so nothing about the links leaves the machine.

**Tags:** dashhub · launcher · macos · bookmarks · browser

## Cool features

- **No network, no leakage.** Monogram/emoji tiles instead of fetched favicons — the link list never hits Google's favicon service or anywhere else.
- **Private config shadows the repo.** `add`/`rm`/`edit` write to `~/.config/dashhub/shortcuts.json` (seeded from the active config on first write), so real links stay out of the git repo while the repo keeps only placeholders.
- **One source of truth.** The same JSON drives the terminal list, the dashhub status line, and the HTML board — no browser-local state to diverge.

## Manage links (CLI verbs)

```bash
shortcuts add "CloudWatch Logs" "https://console.aws.amazon.com/cloudwatch/" -g AWS   # add to a group
shortcuts add Reddit https://reddit.com -e 👽            # emoji tile instead of a monogram
shortcuts edit Reddit --rename r/sysadmin -g Personal    # change name / url / group / emoji
shortcuts edit r/sysadmin -e                             # bare -e clears the emoji
shortcuts rm EKS                                         # remove shortcut(s) by name
```

## View / render

```bash
shortcuts                  # grouped list in the terminal (default)
shortcuts status           # one JSON line {state,headline,detail,asof} for dashhub
shortcuts board            # write + open the HTML grid board
dashhub open shortcuts     # same board, launched via the hub
```

## Config & precedence

```bash
# Read resolution order (first that exists wins):
#   $DASHHUB_SHORTCUTS  →  ~/.config/dashhub/shortcuts.json  →  ~/repos/bin/dashhub.shortcuts.json
# Writes (add/rm/edit) always target ~/.config/dashhub/shortcuts.json unless $DASHHUB_SHORTCUTS is set.

# Config shape — edit by hand too; no code changes needed:
#   { "groups": [ { "name": "AWS", "shortcuts": [ {"name":"Console","url":"https://…","emoji":"☁️"} ] } ] }
# A flat { "shortcuts": [ … ] } also parses (lands in one unnamed group).
```

## Key facts

- Source: `~/repos/bin/shortcuts` (Python, stdlib only). Registered in `~/repos/bin/dashhub.dashboards.json` as key `shortcuts`.
- Board HTML: `~/.local/state/dashhub/shortcuts/board.html`, rewritten in place after every `add`/`rm`/`edit` so the hub's Open link stays fresh.
- `emoji` is optional per shortcut; omit it for a monogram tile. `-e` with no value on `edit` removes it.
