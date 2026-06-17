# grip

Render local markdown using GitHub's own API and serve it on localhost. The output is byte-for-byte what github.com would show — same fonts, same syntax highlighter, same emoji set.

## Cool features

- **GitHub-identical rendering.** No "almost like GitHub" — it *is* GitHub doing the rendering server-side.
- **Cross-file links resolve when you serve a directory.** `grip .` lets relative `.md` links navigate naturally in the browser.
- **Authenticated mode raises rate limit 60 → 5,000 renders/hour.** A `$GITHUB_TOKEN` with no scopes is enough.
- **`--context=user/repo`** makes `#123`, `@mentions`, and `user/repo#456` resolve as if the file lived in that repo.
- **`--user-content`** renders as issue/comment context — enables task lists, @mentions, and other issue-only features.
- **`--export`** writes standalone HTML to disk. Great for one-off shareable docs.
- **Auto-reloads on file change.** Save in your editor, the browser refreshes itself.

## Render and view

```bash
grip                                  # render ./README.md
grip path/to/file.md                  # specific file
grip .                                # serve the whole directory (relative links work)
grip --browser                        # auto-open in default browser
grip -b                               # short form of --browser
grip --quiet                          # suppress the access-log output
```

## Port and bind address

```bash
grip 8080                             # custom port
grip file.md 0.0.0.0:8080             # bind all interfaces — accessible on LAN
grip . 8080 -b                        # serve dir, custom port, auto-open
```

## Authenticated mode (skip the rate limit)

```bash
# One-off
grip --user=billtoner --pass=$GITHUB_TOKEN file.md

# Persistent: put credentials in ~/.grip/settings.py
#   USERNAME = 'billtoner'
#   PASSWORD = 'ghp_xxxxxxxxxxxxxxxx'   # PAT, no scopes needed
```

## Render in a repo's context

```bash
grip --context=billtoner/bt-knowledge-base file.md  # #N, user/repo#N, @mentions resolve
grip --user-content file.md                        # render as comment/issue (task lists, @mentions)
grip --gfm file.md                                  # force GitHub-Flavored Markdown mode
```

## Export to standalone HTML

```bash
grip file.md --export                     # writes file.html alongside the source
grip file.md --export out.html            # explicit output name
grip file.md --export --no-inline         # keep CSS/images external instead of embedding
grip README.md --export --user-content    # export with issue/comment semantics
```

## Quick recipes

```bash
# Preview this repo's index with working navigation
cd ~/Documents/repos/bt-knowledge-base
grip . -b                                 # browse to doc/bt-knowledge-base.md, click around

# Share a one-page rendered note with a coworker
grip notes/postmortem.md --export postmortem.html --no-inline

# View on phone (same Wi-Fi)
grip . 0.0.0.0:8080 -b                    # then visit http://<your-mac-ip>:8080/doc/...
```

## Killer flags

- `-b` / `--browser` — open in default browser
- `--export [file]` — write rendered HTML; `--no-inline` keeps assets external
- `--user-content` — render as issue/comment (task lists, @mentions)
- `--context=<user/repo>` — resolve `#N`, `@user`, `user/repo#N` against that repo
- `--user=` / `--pass=` — authenticate to raise rate limit
- `--norefresh` — stop watching the file for changes
- `--quiet` — suppress request logs
