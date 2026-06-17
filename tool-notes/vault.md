# vault

HashiCorp Vault CLI; auth, KV secrets, dynamic credentials, transit.

## Auth & status

```bash
export VAULT_ADDR=https://vault.corp:8200
vault status                            # sealed? HA? version
vault login -method=oidc                # or token / approle / userpass
vault token lookup                      # current token + its policies
```

## KV secrets (v2)

```bash
vault kv put secret/app api_key="$API_KEY"   # write (value from env, not literal)
vault kv get secret/app                       # read
vault kv get -field=api_key secret/app        # one field — scriptable
vault kv list secret/                         # list keys
```

## Dynamic creds & transit

```bash
vault read database/creds/readonly      # short-lived, auto-revoked DB credentials
vault write transit/encrypt/mykey plaintext=$(base64 <<< "data")   # encryption as a service
```

## Notes

- `-field=` returns a bare value (no formatting) for env injection / scripts
- KV v2 is versioned: `vault kv get -version=3 secret/app`, `vault kv rollback`
