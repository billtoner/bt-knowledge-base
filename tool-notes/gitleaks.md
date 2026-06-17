# gitleaks

Scan repos and files for committed secrets; this repo's pre-commit hook.

## Scan

```bash
gitleaks detect --source . -v          # scan the repo's full git history
gitleaks detect --no-git --source .    # scan files as-is (not history)
gitleaks protect --staged              # pre-commit: scan only staged changes
```

## Output & tuning

```bash
gitleaks detect --report-path leaks.json --report-format json
gitleaks detect --baseline-path baseline.json   # ignore known/accepted findings
gitleaks detect --config .gitleaks.toml         # custom rules / allowlist
```

## Notes

- Wired here via `.pre-commit-config.yaml` (the "Detect hardcoded secrets" hook)
- `protect --staged` is what runs on commit; `detect` walks full history
