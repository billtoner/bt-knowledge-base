# az

Azure CLI — auth, subscriptions, and managing Azure resources.

## Auth & subscriptions

```bash
az login                                 # browser / device-code login
az account show                          # current subscription + tenant
az account list -o table                 # all subscriptions
az account set --subscription "My Sub"   # switch active subscription
```

## Resources & query

```bash
az group list -o table                   # resource groups
az vm list -d -o table                   # VMs with power state (-d shows it)
az vm list --query "[?powerState=='VM running'].name" -o tsv
az resource list --tag env=prod -o table
```

## Handy integrations

```bash
az aks get-credentials -g rg -n cluster  # merge AKS creds into kubeconfig
az acr login -n myregistry               # docker login to a container registry
az monitor activity-log list --offset 1h # recent control-plane events
```

## Killer flags

- `--query "JMESPath"` with `-o table|json|tsv|yaml`
- `--subscription` / `-g, --resource-group`
- `--output none` / `--only-show-errors` — quiet for scripts
