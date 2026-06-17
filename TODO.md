# TODO

Backlog for the next week or so. Check items off as they land; move finished
ones to Done with the date.

## Backlog

_(empty)_

## Done

- 2026-06-16 — Reconciled package/build buckets: renamed `Installing packages` →
  `Package Managers` (OS/global installers: apt, brew, dnf, pacman, snap, pipx)
  and added `Build & Packaging` (project build + language toolchains: make,
  cmake, cargo, npm, uv, poetry). Boundary: installing something to use it →
  Package Managers; building/running a project you wrote (incl. its deps) →
  Build & Packaging.
- 2026-06-16 — Replaced the generic `<Name> tools.` category intros with
  real one-line descriptions across all 17 buckets.

- 2026-06-16 — Re-bucketed to the function-first taxonomy (comprehensive option,
  Title-Case display names). Migrated 66 tools out of 16 old categories into 17
  new ones via `kb move`; added `Containers & Orchestration` and
  `Security & Secrets` placeholders; dropped the redundant `System` placeholder.
- 2026-06-16 — Built `kb move <tool> <category>` (the migration tooling).
- 2026-06-16 — Settled category-name casing: Title Case with spaces (the slug
  carries machine identity, so hyphenation gained nothing). Retires the earlier
  "hyphenate the names" item.
