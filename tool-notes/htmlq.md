# htmlq

jq for HTML; extract content with CSS selectors.

## Extract

```bash
curl -s https://example.com | htmlq 'a' --attribute href   # all link hrefs
curl -s URL | htmlq '.price' --text                        # text of matching nodes
curl -s URL | htmlq 'h1, h2' --text                        # multiple selectors at once
curl -s URL | htmlq '#main' --remove-nodes 'script,style'  # prune noise, keep markup
```

## Notes

- `--text` strips tags; `--attribute X` pulls one attribute; default prints HTML
- Pairs with curl/xh for scraping; feed attribute lists onward into jq
