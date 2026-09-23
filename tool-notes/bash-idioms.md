# bash-idioms

The bash language features that distinguish it from "just typing commands" — parameter expansion, arrays, process substitution, traps, heredocs. Used in scripts and one-liners alike.

**Tags:** shell · scripting

## Cool features

- **Parameter expansion** is a tiny language inside `${...}`: defaults, error-if-unset, substring, search/replace, case change, prefix/suffix strip.
- **Process substitution** `<(cmd)` turns a command's output into a filename — works with anything that wants a file.
- **`set -euo pipefail`** turns silent script bugs into loud failures. Top of every non-trivial script.

## Parameter expansion cheats

```bash
${var:-default}        # use default if var unset or empty
${var:=default}        # use default AND assign it to var
${var:?msg}            # error out with msg if var unset or empty
${var:+alt}            # alt only if var IS set (inverse of :-)
${var#prefix}          # strip shortest matching prefix
${var##prefix}         # strip longest matching prefix          (basename:   ${path##*/})
${var%suffix}          # strip shortest matching suffix
${var%%suffix}         # strip longest matching suffix          (drop ext:   ${file%%.*})
${var/pat/repl}        # first match replace
${var//pat/repl}       # global replace
${var^^}               # upper-case all
${var,,}               # lower-case all
${var:offset:length}   # substring
${#var}                # length
```

## Arrays (indexed and associative)

```bash
arr=(a b c)
echo "${arr[@]}"        # all elements (preserves whitespace per element when quoted)
echo "${#arr[@]}"       # count
arr+=(d)                # append

declare -A m            # associative (hash)
m[host]=db1; m[port]=5432
echo "${m[host]}"
for k in "${!m[@]}"; do echo "$k=${m[$k]}"; done
```

## Process substitution

```bash
diff <(sort file1) <(sort file2)            # diff sorted versions without temp files
comm -23 <(sort a.txt) <(sort b.txt)        # lines unique to a.txt
paste <(cut -f1 a) <(cut -f2 b)             # column-glue from two streams
```

## Brace expansion

```bash
cp file.txt{,.bak}                          # cp file.txt file.txt.bak
mkdir -p project/{src,test,docs}            # three dirs at once
for i in {1..10..2}; do echo $i; done       # 1 3 5 7 9
echo {a,b,c}{1,2}                           # cartesian: a1 a2 b1 b2 c1 c2
```

## Heredocs / here-strings

```bash
cat <<'EOF' > config.yaml
host: db1
port: 5432
EOF
                                            # single-quoted EOF prevents variable expansion

cat <<-EOF                                  # the dash strips leading TABS
	indented heredoc
	doesn't include these tabs
EOF

grep pattern <<<"$variable"                 # here-string: pass a variable as stdin
```

## Read a file line by line, safely

```bash
while IFS= read -r line; do
    printf '%s\n' "$line"
done < file
                                            # IFS= keeps leading/trailing whitespace
                                            # -r prevents backslash interpretation
```

## Traps — guaranteed cleanup

```bash
tmpfile=$(mktemp)
trap 'rm -f "$tmpfile"' EXIT
                                            # runs no matter how the script ends
trap 'echo "got signal at $LINENO"; exit 1' INT TERM
```

## Strict mode

```bash
set -euo pipefail
#    │ │ │  └─ pipe fails if any element fails
#    │ │ └─── error on unset variable
#    │ └───── exit on any error
#    └─────── (only really needed for very old shells)
```

## Conditionals worth knowing

```bash
[[ -f file ]]               # file exists & is regular
[[ -d dir ]]                # directory
[[ -z $var ]]               # empty
[[ -n $var ]]               # non-empty
[[ $a == foo* ]]            # glob match (only in [[ ]], not [ ])
[[ $a =~ ^[0-9]+$ ]]        # regex match
(( a > 5 ))                 # arithmetic context
```
