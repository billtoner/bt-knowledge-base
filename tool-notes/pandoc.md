# pandoc

Universal document converter; markdown / HTML / PDF / docx and dozens more.

## Convert

```bash
pandoc README.md -o readme.html        # markdown -> standalone HTML
pandoc doc.md -o doc.pdf               # -> PDF (needs a LaTeX engine)
pandoc notes.md -o notes.docx          # -> Word
pandoc page.html -t markdown -o page.md   # HTML -> markdown
```

## Polished output

```bash
pandoc doc.md -s --toc -o doc.html     # standalone + table of contents
pandoc doc.md -o doc.pdf --pdf-engine=tectonic
pandoc slides.md -t revealjs -s -o slides.html   # markdown -> reveal.js deck
pandoc -s --css=style.css in.md -o out.html
```

## Notes

- `-s` makes a standalone file (full header/footer), not a fragment
- `-f`/`-t` force input/output formats; templates + `--metadata` give fine control
