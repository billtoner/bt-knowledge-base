# wget

HTTP / FTP downloader with recursive crawling, resumes, and retry policies. Where `curl` is for one-shot requests, `wget` shines at "pull down a tree of files reliably."

**Tags:** http · download · network

## Cool features

- **`-c` resumes interrupted downloads.** Big files over flaky links — just rerun the same command.
- **`-m`** (mirror) bundles `-r -N -l inf --no-remove-listing` — perfect for taking a doc site offline.
- **`-i urls.txt`** downloads a whole list of URLs, one per line.

## Single-file downloads, robustly

```bash
wget -c URL                                  # resume if interrupted
wget --content-disposition URL               # use server-suggested filename
wget --limit-rate=200k URL                   # throttle to 200 KB/s
wget -nv -t 5 -w 2 URL                       # quiet, retry 5×, 2s wait between
```

## Many files

```bash
wget -i urls.txt                             # one URL per line
wget -B https://example.com/ -i paths.txt    # paths.txt has relative paths; -B is the base
```

## Mirror a documentation site offline

```bash
wget -m -p -E -k -np https://example.com/docs/
#     │  │  │  │  └─ no-parent: don't ascend above /docs/
#     │  │  │  └──── convert links to local
#     │  │  └─────── add .html to extensionless served files
#     │  └────────── grab page requisites (CSS, images, JS)
#     └───────────── mirror mode
```

## Pipe a download into another tool

```bash
wget -qO- https://example.com/archive.tar.gz | tar xz -C /tmp/
                                             # straight into tar without a temp file
```

## Authenticated downloads

```bash
wget --user=foo --ask-password URL           # prompts; doesn't echo
wget --header="Authorization: Bearer $TOK" URL
```

## Check links without downloading

```bash
wget --spider -r -l 2 https://example.com/   # crawl 2 levels deep, HEAD-only
                                             # combine with grep for broken-link reports
```

## Killer flags

- `-c` — continue / resume
- `-m` — mirror (shorthand for `-r -N -l inf --no-remove-listing`)
- `-p` — page requisites (for offline rendering)
- `-k` — convert links to local references
- `-np` — no-parent (don't ascend above the start URL's directory)
- `-i FILE` — read URLs from FILE
- `-O FILE` — write to FILE (use `-` for stdout)
- `--limit-rate=N` — throttle
- `--spider` — check, don't download
