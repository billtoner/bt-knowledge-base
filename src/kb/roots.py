"""Knowledge-base roots: the public + private repos kb reads and writes.

Sources, in priority order:
  1. $KB_ROOTS env       — "label=path:label=path"  (or just "path:path")
  2. ~/.config/kb/roots  — one "label = path" (or bare "path") per line; # comments ok
  3. fallback            — supplied by the caller (the repo kb lives in)

The FIRST root is the default write target ("public"); private notes need --private.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_CONFIG = Path.home() / ".config" / "kb" / "roots"


@dataclass(frozen=True)
class Root:
    label: str
    path: Path

    @property
    def notes_dir(self) -> Path:
        return self.path / "tool-notes"

    @property
    def categories_dir(self) -> Path:
        return self.path / "doc" / "categories"

    @property
    def readme(self) -> Path:
        return self.notes_dir / "README.md"

    @property
    def index(self) -> Path:
        """Top-level index: doc/<repo-dir-name>.md, with a doc/*.md fallback."""
        named = self.path / "doc" / f"{self.path.name}.md"
        if named.is_file():
            return named
        docs = sorted((self.path / "doc").glob("*.md"))
        return docs[0] if docs else named

    @property
    def is_private(self) -> bool:
        return "priv" in self.label.lower() or "private" in self.path.name.lower()


def _parse_entry(spec: str) -> Root | None:
    """Parse one "label=path" / "label = path" / "path" entry. Skip unset-up roots."""
    if "=" in spec:
        label, _, path = spec.partition("=")
    else:
        label, path = "", spec
    label, path = label.strip(), path.strip()
    if not path:
        return None
    p = Path(os.path.expanduser(path))
    label = label or p.name
    if not (p / "tool-notes").is_dir():
        return None  # not set up yet
    return Root(label, p)


def load_roots(fallback: Root | None = None) -> list[Root]:
    env = os.environ.get("KB_ROOTS")
    if env:
        specs = env.split(":")
    else:
        cfg = Path(os.environ.get("KB_CONFIG", str(DEFAULT_CONFIG)))
        specs = []
        if cfg.is_file():
            for raw in cfg.read_text().splitlines():
                line = raw.split("#", 1)[0].strip()
                if line:
                    specs.append(line)
    roots = [r for r in (_parse_entry(s) for s in specs) if r is not None]
    if not roots and fallback is not None:
        roots.append(fallback)
    return roots


def root_for(roots: list[Root], sel: str) -> Root | None:
    """Resolve a write target. "" => first (default/public); "priv*" => a private-looking
    root; otherwise an exact label match."""
    if not sel:
        return roots[0] if roots else None
    for r in roots:
        if r.label == sel:
            return r
    if sel.startswith("priv"):
        for r in roots:
            if r.is_private:
                return r
    return None
