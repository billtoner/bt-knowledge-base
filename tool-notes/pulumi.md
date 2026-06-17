# pulumi

Infrastructure as code in real languages; stacks, config, encrypted secrets.

## Stack workflow

```bash
pulumi new aws-typescript              # scaffold a project
pulumi stack init dev                  # create a stack (environment)
pulumi preview                         # diff (like `terraform plan`)
pulumi up                              # apply
pulumi destroy                         # tear the stack down
```

## Config & secrets

```bash
pulumi config set aws:region us-west-2
pulumi config set --secret dbPassword "$DB_PASSWORD"   # encrypted in stack state
pulumi stack output apiUrl             # read an output
pulumi stack select prod               # switch stacks
```

## Inspect

```bash
pulumi stack --show-urns               # resources with their URNs
pulumi refresh                         # reconcile state with real infrastructure
```

## Notes

- Programs are TS/Python/Go/etc. — loops and functions instead of HCL
- Secrets are encrypted per stack; `--secret` keeps them out of plaintext state
