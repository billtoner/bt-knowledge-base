# docker

Build, run, and manage containers and images — plus `docker compose` for stacks.

## Run & exec

```bash
docker run --rm -it --name dbg -p 8080:80 nginx       # foreground, auto-remove, port map
docker run -d --restart=unless-stopped my-image       # detached with a restart policy
docker exec -it dbg bash                               # shell into a running container
docker logs -f --tail=100 dbg                          # follow recent logs
docker stats                                           # live CPU/mem per container
```

## Images & build

```bash
docker build -t app:dev --build-arg VER=1 .           # build and tag
docker buildx build --platform linux/amd64,linux/arm64 -t app:multi --push .   # multi-arch
docker history app:dev                                 # see what made the layers big
docker image prune -f                                  # reclaim dangling layers
```

## Inspect & reclaim space

```bash
docker inspect -f '{{.NetworkSettings.IPAddress}}' dbg # Go-template one field
docker ps -a --format 'table {{.Names}}\t{{.Status}}'  # custom columns
docker system df                                       # disk used by images/containers/volumes
docker system prune -af --volumes                      # reclaim everything unused (careful)
```

## Compose

```bash
docker compose up -d                                   # start the stack detached
docker compose logs -f svc                             # follow one service
docker compose exec svc sh                             # shell into a service
docker compose down -v                                 # stop and remove volumes
```
