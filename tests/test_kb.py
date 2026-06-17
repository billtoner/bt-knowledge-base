from pathlib import Path

import pytest
from typer.testing import CliRunner

from kb import capture, notes
from kb.cli import app
from kb.roots import Root, root_for

runner = CliRunner()

SSH_NOTE = """\
# ssh

secure shell.

## Forwarding

```bash
ssh -L 8080:localhost:80 host    # local port forward
```

## Jump hosts

```bash
ssh -J jump user@target          # via bastion
```
"""


@pytest.fixture
def repo(tmp_path: Path) -> Root:
    (tmp_path / "tool-notes").mkdir()
    (tmp_path / "doc" / "categories").mkdir(parents=True)
    (tmp_path / "doc" / f"{tmp_path.name}.md").write_text(
        "# index\n\n## Categories\n\n- [Network](categories/network.md)\n"
    )
    (tmp_path / "doc" / "categories" / "network.md").write_text(
        "# Network\n\nNetwork tools.\n\n- [ssh](../../tool-notes/ssh.md) — secure shell\n"
    )
    (tmp_path / "tool-notes" / "ssh.md").write_text(SSH_NOTE)
    (tmp_path / "tool-notes" / "README.md").write_text(
        "# tool-notes\n\nstuff\n\n## Tools\n\n- [ssh](ssh.md) — secure shell\n"
    )
    (tmp_path / "tool-notes" / "orphan.md").write_text("# orphan\n\nnot filed.\n")
    return Root(tmp_path.name, tmp_path)


def test_kebab():
    assert capture.kebab("AWS CLI") == "aws-cli"
    assert capture.kebab("File and Directory") == "file-and-directory"
    assert capture.kebab("  Spaced  ") == "spaced"


def test_list_categories(repo: Root):
    cats = notes.list_categories(repo)
    assert [c.name for c in cats] == ["Network"]
    assert [t.slug for t in cats[0].tools] == ["ssh"]
    assert cats[0].tools[0].desc == "secure shell"


def test_orphans(repo: Root):
    cats = notes.list_categories(repo)
    assert notes.orphan_tools(repo, cats) == ["orphan"]


def test_find_command_rank(repo: Root):
    res = notes.find([repo], ["ssh"])
    assert len(res) == 2
    assert all(e.rank == 2 for e in res)  # 'ssh' is in the command itself


def test_find_via_intent(repo: Root):
    res = notes.find([repo], ["forward"])
    assert len(res) == 1
    e = res[0]
    assert e.rank == 1  # matched through the intent, not the command
    assert e.line == 8
    assert e.section == "Forwarding"
    assert e.intent == "# local port forward"


def test_find_no_match(repo: Root):
    assert notes.find([repo], ["nonexistent-term"]) == []


def test_find_insert_line():
    assert capture.find_insert_line(SSH_NOTE, "Jump hosts") == 15
    assert capture.find_insert_line(SSH_NOTE, "Forwarding") == 9
    assert capture.find_insert_line(SSH_NOTE, "") == 15  # last block
    assert capture.find_insert_line(SSH_NOTE, "Nonexistent") == 0


def test_insert_template(repo: Root):
    note = repo.notes_dir / "ssh.md"
    capture.insert_template(note, capture.find_insert_line(SSH_NOTE, "Forwarding"))
    lines = note.read_text().splitlines()
    assert lines[8] == capture.TEMPLATE  # inserted at line 9 (0-based index 8)
    assert lines[9] == "```"  # the closing fence shifted down


def test_add_category_bullet_existing(repo: Root):
    cat = repo.categories_dir / "network.md"
    created = capture.add_category_bullet(cat, "Network", "scp", "secure copy")
    assert created is False
    assert "- [scp](../../tool-notes/scp.md) — secure copy" in cat.read_text()


def test_add_category_bullet_new_and_wire(repo: Root):
    cat = repo.categories_dir / "search.md"
    created = capture.add_category_bullet(cat, "Search", "rg", "fast grep")
    assert created is True
    assert cat.read_text().startswith("# Search")
    capture.wire_index_category(repo.index, "Search", "search")
    index = repo.index.read_text()
    # Search sorts after Network, so the link lands after it.
    assert index.index("[Network]") < index.index("[Search]")
    assert "- [Search](categories/search.md)" in index


def test_wire_index_alpha_before(repo: Root):
    capture.wire_index_category(repo.index, "Audio", "audio")
    index = repo.index.read_text()
    assert index.index("[Audio]") < index.index("[Network]")


def test_add_readme_bullet_alpha(repo: Root):
    capture.add_readme_bullet(repo, "curl", "http client")
    readme = repo.readme.read_text()
    # curl sorts before ssh
    assert readme.index("[curl]") < readme.index("[ssh]")


def test_list_categories_flag_matches_cats(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    flag = runner.invoke(app, ["list", "--categories"])
    sub = runner.invoke(app, ["cats"])
    assert flag.exit_code == 0
    assert sub.exit_code == 0
    assert flag.output == sub.output
    assert "Network" in flag.output
    # the -c short form is equivalent
    assert runner.invoke(app, ["list", "-c"]).output == flag.output


def test_move_to_new_category_empties_old(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["move", "ssh", "Remote Access"])
    assert r.exit_code == 0
    new = repo.categories_dir / "remote-access.md"
    assert new.exists()
    assert "- [ssh](../../tool-notes/ssh.md) — secure shell" in new.read_text()
    # Network had only ssh, so it's emptied and removed, and unlinked from the index.
    assert not (repo.categories_dir / "network.md").exists()
    index = repo.index.read_text()
    assert "network.md" not in index
    assert "remote-access.md" in index


def test_move_keeps_nonempty_source(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    # A source category with two tools; moving one leaves the other behind.
    (repo.notes_dir / "scp.md").write_text("# scp\n\ncopy.\n")
    (repo.notes_dir / "rsync.md").write_text("# rsync\n\nsync.\n")
    (repo.categories_dir / "transfer.md").write_text(
        "# Transfer\n\nTransfer tools.\n\n"
        "- [scp](../../tool-notes/scp.md) — copy\n"
        "- [rsync](../../tool-notes/rsync.md) — sync\n"
    )
    r = runner.invoke(app, ["move", "scp", "Network"])
    assert r.exit_code == 0
    transfer = repo.categories_dir / "transfer.md"
    assert transfer.exists()  # not emptied
    assert "rsync" in transfer.read_text()
    assert "scp" not in transfer.read_text()
    assert "scp" in (repo.categories_dir / "network.md").read_text()


def test_move_already_there(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["move", "ssh", "Network"])
    assert r.exit_code == 0
    assert "already in" in r.output


def test_move_unknown_tool(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["move", "nope", "Network"])
    assert r.exit_code == 1


def test_move_dry_run_writes_nothing(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    before = (repo.categories_dir / "network.md").read_text()
    r = runner.invoke(app, ["move", "ssh", "Remote Access", "--dry-run"])
    assert r.exit_code == 0
    assert "DRY-RUN" in r.output
    assert (repo.categories_dir / "network.md").read_text() == before
    assert not (repo.categories_dir / "remote-access.md").exists()


def test_list_sections():
    assert notes.list_sections(SSH_NOTE) == ["Forwarding", "Jump hosts"]


def test_add_section(repo: Root):
    note = repo.notes_dir / "ssh.md"
    line = capture.add_section(note, "Tunnels")
    text = note.read_text()
    assert notes.list_sections(text)[-1] == "Tunnels"
    assert text.splitlines()[line - 1] == capture.TEMPLATE  # editor lands on the template


def test_sections_command(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["sections", "ssh"])
    assert r.exit_code == 0
    assert r.output.splitlines() == ["Forwarding", "Jump hosts"]


def test_add_new_section(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    monkeypatch.setenv("EDITOR", "true")  # no-op so open_at doesn't launch an editor
    r = runner.invoke(app, ["add", "ssh", "--new-section", "Tunnels"])
    assert r.exit_code == 0
    assert "## Tunnels" in (repo.notes_dir / "ssh.md").read_text()


def test_add_new_section_existing_errors(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    monkeypatch.setenv("EDITOR", "true")
    r = runner.invoke(app, ["add", "ssh", "--new-section", "Forwarding"])
    assert r.exit_code == 1


def test_list_verbose_shows_sections(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["list", "-v"])
    assert r.exit_code == 0
    assert "Forwarding" in r.output and "Jump hosts" in r.output


def test_cats_verbose_shows_counts(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["cats", "-v"])
    assert r.exit_code == 0
    assert "Network  (1)" in r.output


def test_root_for():
    pub = Root("pub", Path("/tmp/pub"))
    priv = Root("private", Path("/tmp/private"))
    roots = [pub, priv]
    assert root_for(roots, "") is pub
    assert root_for(roots, "private") is priv
    assert root_for(roots, "priv") is priv
    assert root_for(roots, "nope") is None
