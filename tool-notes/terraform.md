# terraform

Provision infrastructure as code; plan, apply, state, workspaces.

## Core loop

```bash
terraform init                         # download providers, configure the backend
terraform fmt -recursive               # canonical formatting
terraform validate                     # static checks
terraform plan -out=tf.plan            # preview changes; save the plan
terraform apply tf.plan                # apply exactly what you reviewed
```

## State & targeting

```bash
terraform state list                   # resources tracked in state
terraform state show aws_instance.web  # one resource's attributes
terraform apply -target=module.db      # apply a subset (use sparingly)
terraform import aws_s3_bucket.b name  # adopt existing infra into state
terraform state rm aws_instance.gone   # forget a resource (no destroy)
```

## Workspaces & output

```bash
terraform workspace new staging        # per-environment state
terraform output -json                 # machine-readable outputs
terraform show -json tf.plan | jq      # inspect a saved plan
```

## Killer flags

- `-out=FILE` then `apply FILE` — review then apply the exact plan
- `-target=ADDR` scopes an op; `-replace=ADDR` forces recreate
- `-var 'k=v'` / `-var-file=prod.tfvars`
- `TF_LOG=DEBUG` — provider/debug logging
