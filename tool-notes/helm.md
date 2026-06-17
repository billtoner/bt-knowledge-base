# helm

Kubernetes package manager — install, template, and manage chart releases.

## Repos & search

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update                           # refresh repo indexes
helm search repo postgres                  # charts matching a term
helm search hub ingress-nginx              # search Artifact Hub
```

## Install / upgrade / rollback

```bash
helm install myrel bitnami/redis -n data --create-namespace
helm upgrade --install myrel bitnami/redis -f values.yaml --atomic --wait
helm history myrel -n data                 # release revisions
helm rollback myrel 1 -n data              # revert to revision 1
helm uninstall myrel -n data
```

## Inspect & debug

```bash
helm list -A                               # releases across all namespaces
helm template myrel bitnami/redis -f values.yaml   # render manifests locally (no apply)
helm get values myrel -n data              # values a release was installed with
helm upgrade myrel bitnami/redis --dry-run --debug -f values.yaml   # validate without applying
```

## Killer flags

- `--atomic` — roll back automatically if an upgrade fails
- `--wait --timeout 5m` — block until resources are Ready
- `-f values.yaml` / `--set key=value` — override chart values
- `-n <ns> --create-namespace` — scope a release to a namespace
