# aws

AWS CLI v2 — auth profiles and every service API from the shell.

## Profiles & auth

```bash
aws configure --profile work            # set keys/region for a named profile
aws sso login --profile work            # IAM Identity Center (SSO) login
aws sts get-caller-identity             # who am I / which account
export AWS_PROFILE=work                  # default profile for the session
```

## Common reads

```bash
aws s3 ls s3://my-bucket/                # list (s3 high-level commands)
aws s3 sync ./dir s3://my-bucket/dir     # mirror a directory up to S3
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name]' --output table
aws logs tail /aws/lambda/fn --follow    # live CloudWatch logs
```

## Filtering output

```bash
aws ec2 describe-instances --filters Name=instance-state-name,Values=running
aws ec2 describe-instances --query 'Reservations[].Instances[].PublicIpAddress' --output text
aws --output json ec2 describe-vpcs | jq '.Vpcs[].VpcId'
```

## Killer flags

- `--profile` / `--region` — per-command overrides
- `--query 'JMESPath'` — client-side filtering without piping to jq
- `--output json|table|text|yaml`
- `--no-cli-pager` — stop paginating into less
- `--dry-run` — many EC2 mutating calls validate permissions without acting
