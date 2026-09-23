# git

The version control system itself — focused on the commands and flags that are easy to forget between uses.

**Tags:** git

## Cool features

- **`--force-with-lease`** refuses to push if someone else has updated the remote since you last fetched. Use this instead of `--force`; same effect, won't clobber a teammate.
- **`git worktree add`** lets you check out a second branch in a separate directory *without* cloning again. Perfect for "I need to peek at main while my feature branch is half-done."
- **`git reflog`** is the safety net. Every HEAD movement (commit, reset, rebase, checkout) is logged for ~90 days. If you "lost" work, it's almost certainly here.
- **`git bisect run <cmd>`** automates the binary search — run a test command at each step, git picks the next commit.
- **`git restore --staged`** is the modern way to unstage a file. No more remembering `git reset HEAD <file>`.
- **`git switch`** is the modern verb for changing branches; `git checkout` is overloaded with too many meanings.
- **`git log --oneline --graph --all --decorate`** is the one log incantation worth aliasing — see the whole graph at a glance.
- **`git diff --word-diff`** highlights changed *words* on a line, not whole lines. Surprisingly useful for prose or config files.

## Stash recipes

```bash
git stash push -m "WIP: refactoring auth"           # named stash (easier to find later)
git stash push -m "...just this file" path/to/file  # stash specific paths only
git stash --keep-index                              # stash unstaged changes only
git stash list                                      # all stashes with messages
git stash show -p stash@{2}                         # diff for a specific stash
git stash apply stash@{2}                           # apply without dropping
git stash pop                                       # apply + drop the top stash
git stash drop stash@{2}                            # delete specific stash
git stash clear                                     # nuke all stashes
```

## Log / history recipes

```bash
git log --oneline --graph --all --decorate          # the visual graph
git log --since "2 weeks ago" --author "wtoner"     # filter by time + author
git log -p path/to/file                             # full diff history for one file
git log -S "function_name"                          # commits that add/remove the string
git log -L :func_name:path/to/file.py               # history of one function over time
git log master..feature                             # commits on feature not on master
git log --grep="fix" --oneline                      # search commit messages
git log --pretty=format:"%h %an %ar %s"             # custom one-line format
git shortlog -sn                                    # commit count per author (leaderboard)
```

## Diff recipes

```bash
git diff                                            # unstaged changes
git diff --cached         # (== --staged)           # staged changes
git diff HEAD                                       # everything not in HEAD
git diff main...feature                             # three-dot: diff since branch point
git diff main..feature                              # two-dot: state-to-state
git diff --word-diff                                # word-level highlighting
git diff --stat                                     # file-level summary only
git diff --name-only                                # just changed filenames
git diff HEAD~3 HEAD -- path/to/file                # diff one file over last 3 commits
```

## Undo / recovery

```bash
# Unstage a file (modern)
git restore --staged path/to/file
git restore path/to/file                            # discard unstaged changes (DESTRUCTIVE)

# Reset variants
git reset --soft HEAD~1                             # undo commit, keep changes staged
git reset --mixed HEAD~1   # (default)              # undo commit, keep changes unstaged
git reset --hard HEAD~1                             # DESTRUCTIVE — discards changes

# Recover "lost" work via reflog
git reflog                                          # every HEAD move (last ~90 days)
git checkout HEAD@{2}                               # peek at a prior HEAD state
git reset --hard HEAD@{2}                           # restore to that state

# Amend the last commit
git commit --amend                                  # edit message + add staged changes
git commit --amend --no-edit                        # add staged changes, keep message
```

## Worktrees (multiple branches checked out at once)

```bash
git worktree add ../proj-hotfix hotfix-1.2          # new dir, checked out to hotfix-1.2
git worktree add ../proj-main main                  # main branch in a sibling dir
git worktree list                                   # all active worktrees
git worktree remove ../proj-hotfix                  # clean up when done
git worktree prune                                  # forget worktrees whose dirs are gone
```

## Bisect (binary-search for the breaking commit)

```bash
git bisect start
git bisect bad                                      # current commit is broken
git bisect good v1.2.0                              # this version was fine
# git checks out the midpoint; test, then:
git bisect good   # or bad
# ...repeat...
git bisect reset                                    # back to HEAD when done

# Automated:
git bisect start HEAD v1.2.0
git bisect run pytest tests/test_thing.py           # git drives the whole thing
```

## Rebase

```bash
git rebase main                                     # replay feature on top of main
git rebase -i HEAD~5                                # interactive: reorder/squash/edit last 5
git rebase --continue                               # after fixing conflicts
git rebase --abort                                  # bail out entirely
git pull --rebase                                   # fetch + rebase (cleaner than merge pulls)
git config --global pull.rebase true                # make --rebase the default
```

## Branch / switch

```bash
git switch feature-x                                # change branch (modern verb)
git switch -c new-branch                            # create and switch
git switch -                                        # toggle to previous branch
git branch -d feature-x                             # delete merged branch
git branch -D feature-x                             # force delete (unmerged) — DESTRUCTIVE
git branch -a                                       # all branches incl. remote
git branch -vv                                      # show tracking info
```

## Remote management

```bash
git remote -v                                       # list remotes
git remote add upstream git@github.com:org/repo.git
git remote set-url origin git@github.com:me/repo.git    # switch HTTPS → SSH
git remote rename origin oldorigin
git fetch --all --prune                             # update everything, drop deleted branches
```

## Push safely

```bash
git push                                            # default
git push -u origin feature                          # first push: set upstream
git push --force-with-lease                         # safer force-push (refuses if remote moved)
git push origin --tags                              # push all tags
git push origin v1.2.0                              # push one tag
git push origin --delete branchname                 # delete remote branch
```

## Inspection

```bash
git blame -w -C path/to/file                        # blame ignoring whitespace + copy-detection
git blame -L 50,80 path/to/file                     # blame a line range only
git show HEAD~3:path/to/file                        # contents of a file at a past commit
git show <sha> --stat                               # commit summary + file list
git rev-parse HEAD                                  # full SHA of HEAD
git rev-parse --short HEAD                          # short SHA
git rev-parse --abbrev-ref HEAD                     # current branch name
```

## Clean (untracked files)

```bash
git clean -n                                        # dry run — what would be removed
git clean -fd                                       # remove untracked files + dirs (DESTRUCTIVE)
git clean -fdx                                      # also remove .gitignored files
```

## Aliases worth setting

```bash
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.st "status -sb"
git config --global alias.co "checkout"
git config --global alias.cm "commit -m"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "restore --staged"
```

## Killer flags

- `--force-with-lease` — safer force-push
- `-p` on `log`, `stash show`, `git add` — show/select patches interactively
- `--no-pager` — print to stdout instead of paging (great for scripts)
- `-C <dir>` — operate on a different repo without `cd`
- `--cached` / `--staged` — operate on the index, not the working tree
- `--word-diff` — word-level diff highlighting
- `--name-only` / `--stat` — collapse diff output to summaries
