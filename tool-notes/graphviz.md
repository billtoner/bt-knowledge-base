# graphviz

Diagrams as code; render DOT graphs to SVG/PNG with `dot` and friends.

## Render

```bash
dot -Tsvg graph.dot -o graph.svg       # directed graph -> SVG
dot -Tpng -Gdpi=150 graph.dot -o g.png # PNG at higher DPI
echo 'digraph{a->b->c; a->c}' | dot -Tsvg -o quick.svg   # inline graph
```

## Layout engines

- `dot` — hierarchical (default, for DAGs)
- `neato` / `fdp` — force-directed (undirected graphs)
- `circo` — circular; `twopi` — radial

## Notes

- `-T` output format; `-G`/`-N`/`-E` set graph/node/edge attributes
- Many tools emit DOT (e.g. `terraform graph`) — pipe it straight into `dot`
