# parted

Partition disks — `parted` (scriptable) and `fdisk` (interactive).

## Inspect

```bash
sudo parted -l                         # all disks + their partition tables
sudo parted /dev/sdb print             # one disk's layout
sudo fdisk -l /dev/sdb                 # classic listing
lsblk /dev/sdb                         # quick tree view
```

## Modify (destructive — be sure of the device)

```bash
sudo parted /dev/sdb mklabel gpt       # new GPT partition table
sudo parted -a opt /dev/sdb mkpart primary ext4 0% 100%   # one full-disk partition
sudo fdisk /dev/sdb                    # interactive: n new, d delete, p print, w write
```

## Notes

- Confirm the target with `lsblk` / `parted -l` first — the wrong device is data loss
- After partitioning: `mkfs.ext4 /dev/sdb1`, then `blkid` for the new UUID
