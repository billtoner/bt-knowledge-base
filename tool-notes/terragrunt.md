# terragrunt

Keep Terraform DRY across environments; generated backend/provider config and
dependency-ordered runs.

## Run like terraform

```bash
terragrunt plan                        # wraps `terraform plan` with generated config
terragrunt apply
terragrunt output
```

## Across many modules

```bash
terragrunt run-all plan                # every module under here, dependency-ordered
terragrunt run-all apply
terragrunt graph-dependencies          # emit the dependency graph (DOT)
```

## Handy

```bash
terragrunt hclfmt                      # format terragrunt.hcl files
terragrunt state list                  # passthrough to `terraform state`
```

## Notes

- One `terragrunt.hcl` per env generates backend + provider blocks — no copy-paste
- `run-all` walks a tree; mind cross-module dependencies before applying
- `--terragrunt-log-level debug` when wiring/state misbehaves
