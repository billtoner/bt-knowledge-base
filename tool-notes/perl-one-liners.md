# perl-one-liners

`perl -pe`, `-ne`, `-lane`. The original swiss army knife for stream editing — many things `sed`/`awk` make awkward become one short line in perl.

**Tags:** scripting · one-liners · perl · text

## Cool features

- **`-i`** edits files in place; `-i.bak` keeps a backup. Trivial bulk renames and fixups.
- **`-a`** auto-splits each line into `@F` (like awk). `-F:` sets the delimiter.
- **`-l`** chomps input lines and adds `\n` to `print`. Combined with `-n`/`-p`, you stop fighting newlines.

## Substitution (sed-like, but PCRE)

```bash
perl -pe 's/foo/bar/g' file                       # like sed; reads stdin or files
perl -i -pe 's/foo/bar/g' *.txt                   # in-place across many files
perl -i.bak -pe 's/\bfoo\b/bar/g' file.txt        # in-place with backup; word-boundary regex
perl -pe 's/(\d{3})-(\d{4})/$1.$2/g' phones.txt   # capture groups in the replacement
```

## Grep-like extraction

```bash
perl -ne 'print if /pattern/' file                # grep
perl -ne 'print if /ERROR/ .. /^---$/' log        # range: from ERROR to next "---"
perl -nE 'say if 1..10' file                      # first 10 lines (head -n10)
perl -nE 'say if eof' file                        # just the last line (tail -n1)
```

## Field manipulation (awk-like)

```bash
perl -lane 'print $F[2]' file                     # 3rd field, whitespace-split
perl -F: -lane 'print $F[0]' /etc/passwd          # usernames; : delimiter
perl -lane 'print "$F[-1] $F[0]"' file            # last field, then first
perl -lane '$s+=$F[1]; END{print $s}' file        # sum column 2
```

## sort | uniq -c | sort -rn in one line

```bash
perl -lne '$h{$_}++; END{print "$h{$_}\t$_" for sort{$h{$b}<=>$h{$a}} keys %h}' file
```

## Slurp / paragraph modes

```bash
perl -0777 -pe 's/\nfoo\n/BAR/g' file             # -0777 slurps the whole file as one string
perl -00 -nE 'say if /pattern/' file              # paragraph mode (blank-line delimited records)
```

## Things sed/awk can't do easily

```bash
perl -ne 'print scalar reverse' file              # reverse each line, char-by-char
perl -lne 'print uc' file                         # upper-case each line
perl -nE 'chomp; say length, " $_"' file          # line length + line
perl -0777 -pE 'BEGIN{undef $/} s/(\w+)\s+\1/[DUP $1]/g' file
                                                  # find adjacent duplicate words across line breaks
```

## Killer flags

- `-e 'CODE'` — code to run
- `-p` — loop, print each line after
- `-n` — loop, don't auto-print
- `-i[ext]` — in-place edit (optional backup extension)
- `-a` — auto-split into `@F`
- `-F<sep>` — field separator for `-a`
- `-l` — chomp inputs, add `\n` to `print`
- `-0<oct>` — input record separator (`-0777` slurp, `-00` paragraph)
- `-E` — like `-e` but enables modern features (`say`, etc.)
