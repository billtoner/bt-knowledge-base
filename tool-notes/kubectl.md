# kubectl

The Kubernetes control-plane CLI — query and manage cluster resources.

## Pods that aren't Running (all namespaces)

```bash
kubectl get pods --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.status.phase}{"\t"}{.spec.containers[*].image}{"\n"}{end}' | awk '$3 != "Running"' | column -t -s $'\t'   # ns, name, phase, image — anything not Running, as a table
```
