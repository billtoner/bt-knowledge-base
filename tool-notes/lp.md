# lp (`lp` / `lpr`)

Print files from the command line via CUPS — the same print system macOS and most Linux use under the GUI.

**Tags:** printing · cups · macos · linux

## Cool features

- **It's already there.** macOS and most Linux ship CUPS; `lp` submits straight to the same queues the GUI uses. No extra install.
- **Prints what CUPS can rasterize directly.** PDF, PostScript, plain text, JPEG/PNG go straight through. Convert anything else (e.g. `.docx`) to PDF first — it won't render those natively.
- **The printer must already be added** (System Settings → Printers, or `lpadmin`). `lp` only submits to queues CUPS already knows; it won't discover a new printer.

## Print a file

```bash
lp myfile.pdf                         # to the default printer
lpr myfile.pdf                        # same, BSD-style
lp -d EPSON_XP_XXXX myfile.pdf        # to a named printer
echo "hello" | lp                     # print from stdin
```

## Find printers / pick the right queue name

```bash
lpstat -p -d                          # list printers + show the default
lpstat -a                             # queues accepting jobs
lpoptions -p EPSON_XP_XXXX -l         # list a printer's options + current defaults
```

## Common print options (`-o`)

```bash
lp -n 2 file.pdf                             # 2 copies
lp -o sides=two-sided-long-edge file.pdf     # duplex (long edge)
lp -o sides=two-sided-short-edge file.pdf    # duplex (short edge / flip)
lp -o media=Letter file.pdf                  # paper size (or A4, Legal)
lp -o fit-to-page file.pdf                   # scale to the page
lp -o landscape file.pdf                     # rotate
lp -P 1-3 file.pdf                           # page range (1-3)
lp -o page-ranges=2,4-6 file.pdf             # specific pages
lp -o ColorModel=Gray file.pdf               # force grayscale (name varies by driver)
```

## Manage the queue

```bash
lpstat -o                             # jobs waiting, with job IDs
lpstat -W completed                   # recently finished jobs
cancel EPSON_XP_XXXX-42               # cancel one job by ID
cancel -a EPSON_XP_XXXX               # cancel all jobs on a printer
lpstat -t                             # everything: printers, defaults, jobs
```

## Set a default printer

```bash
lpoptions -d EPSON_XP_XXXX            # make this the default queue
```

## Killer flags

- `-d <printer>` — target a specific queue (name from `lpstat -p`)
- `-n <count>` — number of copies
- `-o <key=value>` — any driver/CUPS option; `lpoptions -p <printer> -l` lists valid ones
- `-P <range>` — page range to print
