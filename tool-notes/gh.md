# gh

GitHub from the terminal; PRs, issues, releases, Actions, and the raw API.

## Pull requests

```bash
gh pr create --fill                    # PR from the current branch (title/body from commits)
gh pr status                           # your PRs + review requests
gh pr checkout 123                     # check out a PR locally
gh pr view 123 --web                   # open it in the browser
gh pr merge 123 --squash --delete-branch
```

## Issues & repos

```bash
gh issue list --label bug --state open
gh issue create -t "title" -b "body"
gh repo clone owner/repo
gh repo view --web
```

## Actions & API

```bash
gh run list                            # recent workflow runs
gh run watch                           # live-tail the latest run
gh api repos/{owner}/{repo}/pulls --jq '.[].title'   # raw API piped through jq
gh auth status                         # who am I, which host
```

## Notes

- `gh pr create --fill` is the fast path; `--web` opens almost anything in a browser
- `gh api ... --jq` scripts directly against the GitHub API
