# lsblk

Block devices, partitions, mounts, and sizes as a tree.

## Use it

```bash
lsblk                                  # tree of disks + partitions
lsblk -f                               # add FSTYPE, LABEL, UUID, MOUNTPOINT
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,MODEL   # choose columns
lsblk -p                               # full device paths (/dev/sda1)
```

## Scripting

```bash
lsblk -J                               # JSON output
lsblk -dn -o NAME,SIZE                  # disks only, no header
lsblk -b                               # sizes in exact bytes
```

## Notes

- `-f` is the fast way to see filesystems + UUIDs for `/etc/fstab`
- Pairs with `blkid` (UUIDs/types) and `findmnt` (the mount tree)
