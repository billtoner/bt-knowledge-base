# gcloud

Google Cloud CLI — auth, configuration, and managing GCP resources.

## Auth & config

```bash
gcloud auth login                         # browser OAuth for your user account
gcloud auth application-default login     # ADC for local SDKs / Terraform
gcloud auth list                          # which accounts are authenticated
gcloud config configurations list         # named config profiles
gcloud config set project my-proj         # switch active project
gcloud config set account me@corp.com     # switch active account
gcloud info                               # SDK paths, active config, versions
```

## Service accounts & tokens

```bash
gcloud auth activate-service-account --key-file=sa.json   # CI / automation
gcloud auth print-access-token                            # bearer token for curl
gcloud auth print-identity-token                          # OIDC token (Cloud Run, IAP)
```

## Inspecting resources

```bash
gcloud projects list                                      # projects you can see
gcloud compute instances list                             # VMs across zones
gcloud compute ssh my-vm --zone=us-central1-a --tunnel-through-iap   # SSH with no public IP
gcloud logging read 'severity>=ERROR' --limit=20 --freshness=1h      # recent errors
```

## Killer flags

- `--project` / `--account` / `--configuration` — override active config per command
- `--format=json|yaml` or `--format="value(name)"` — script-friendly output
- `--filter='labels.env=prod'` — narrow results
- `--impersonate-service-account=SA` — act as an SA without downloading a key
