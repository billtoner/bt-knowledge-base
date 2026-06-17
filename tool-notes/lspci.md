# lspci

List PCI devices; bound drivers, IDs, and bus topology.

## Use it

```bash
lspci                                  # one line per device
lspci -k                               # show the kernel driver + modules in use
lspci -nn                              # include numeric vendor:device IDs
lspci -vv -s 00:02.0                   # verbose details for one device (its BDF)
```

## Notes

- `-k` answers "which driver is bound?"; `-nn` gives IDs for driver hunting
- `lspci -tv` draws the bus tree; companions: `lsusb`, `lshw`, `lscpu`
