# tailscale

WireGuard-based mesh VPN; MagicDNS, ACLs, and zero-config peer connectivity.

## Connect & status

```bash
tailscale up                           # log in / bring this node onto your tailnet
tailscale status                       # peers, IPs, online state
tailscale ip -4                        # this node's tailnet IP
tailscale ping host                    # latency to a peer (direct vs relayed)
```

## Useful modes

```bash
tailscale up --ssh                     # allow Tailscale SSH into this node
tailscale up --advertise-routes=10.0.0.0/24   # act as a subnet router (needs approval)
tailscale up --advertise-exit-node     # offer this node as an exit node
tailscale set --exit-node=host         # route all egress through a peer
```

## Notes

- `tailscale netcheck` diagnoses NAT / DERP-relay issues
- `tailscale file cp` sends files peer-to-peer (Taildrop)
