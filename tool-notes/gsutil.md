# gsutil

Google Cloud Storage from the command line — `gsutil`, and the newer, faster
`gcloud storage` equivalents.

## Everyday object ops

```bash
gsutil ls gs://my-bucket/                  # list objects
gsutil ls -l gs://my-bucket/**             # recursive, with sizes
gsutil cp file.txt gs://my-bucket/         # upload
gsutil cp gs://my-bucket/file.txt .        # download
gsutil cat gs://my-bucket/log.txt          # stream to stdout
```

## Fast bulk transfer & sync

```bash
gsutil -m cp -r ./dir gs://my-bucket/dir   # -m = parallel/multithreaded
gsutil -m rsync -r -d ./local gs://b/x     # mirror; -d deletes extras at the dest
gcloud storage cp -r ./dir gs://my-bucket/ # newer CLI, generally faster
gcloud storage rsync -r ./local gs://b/x   # newer rsync
```

## Metadata, access, signed URLs

```bash
gsutil stat gs://my-bucket/file            # size, hashes, content-type, metadata
gsutil signurl -d 1h sa-key.json gs://b/f  # time-limited download URL
gsutil iam ch user:me@x.com:objectViewer gs://b   # grant bucket access
gsutil du -sh gs://my-bucket               # total size of a bucket/prefix
```

## Killer flags

- `-m` — parallelize; the single biggest speedup for many objects
- `gcloud storage` — prefer for new work; faster and the actively-developed path
- `rsync -d` — make the destination match the source (deletes); test without `-d` first
