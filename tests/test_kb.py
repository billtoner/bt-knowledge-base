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
    # two command lines (rank 2) + the description prose line (rank 0, via the title)
    cmds = [e for e in res if e.kind == "cmd"]
    prose = [e for e in res if e.kind == "prose"]
    assert len(cmds) == 2 and all(e.rank == 2 for e in cmds)
    assert len(prose) == 1 and prose[0].rank == 0
    assert res[0].rank == 2 and res[-1].rank == 0  # commands rank above prose


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


def test_show_command(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["show", "ssh"])
    assert r.exit_code == 0
    assert "# ssh" in r.output
    assert "## Forwarding" in r.output


def test_show_unknown_tool(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["show", "nope"])
    assert r.exit_code == 1


def test_note_tags_parsing():
    # middot separator, mixed case, and a code fence that must be ignored
    text = (
        "# rg\n\ngrep replacement.\n\n"
        "**Tags:** Search · Text · search\n\n"
        "```bash\n**Tags:** nope\n```\n"
    )
    assert notes.note_tags(text) == ["search", "text"]  # deduped, lowercased, fence skipped
    # comma separator also works
    assert notes.note_tags("# x\n\nd\n\n**Tags:** a, b, c\n") == ["a", "b", "c"]
    # no tag line
    assert notes.note_tags("# x\n\njust a description\n") == []


def test_tag_line_render():
    assert capture.tag_line(["Search", "modern unix", "search"]) == "**Tags:** search · modern-unix"
    assert capture.tag_line([]) == ""


def _tag_ssh(repo: Root, tags: str = "remote · shell") -> None:
    """Add a **Tags:** line to the fixture's ssh note."""
    note = repo.notes_dir / "ssh.md"
    note.write_text(SSH_NOTE.replace("secure shell.", f"secure shell.\n\n**Tags:** {tags}"))


def test_collect_tags(repo: Root):
    _tag_ssh(repo)
    tagged = notes.collect_tags([repo])
    assert len(tagged) == 1
    tt = tagged[0]
    assert tt.slug == "ssh"
    assert tt.category == "Network"
    assert tt.desc == "secure shell"
    assert tt.tags == ("remote", "shell")


def test_tags_command(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    _tag_ssh(repo)
    r = runner.invoke(app, ["tags"])
    assert r.exit_code == 0
    assert r.output.splitlines() == ["remote", "shell"]
    rv = runner.invoke(app, ["tags", "-v"])
    assert "remote  (1)" in rv.output


def test_tag_query_and_intersection(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    _tag_ssh(repo)
    (repo.notes_dir / "mosh.md").write_text("# mosh\n\nroaming shell.\n\n**Tags:** remote\n")
    single = runner.invoke(app, ["tag", "remote"])
    assert single.exit_code == 0
    assert "ssh" in single.output and "mosh" in single.output
    # intersection: only ssh has both
    both = runner.invoke(app, ["tag", "remote", "shell"])
    assert both.exit_code == 0
    assert "ssh" in both.output and "mosh" not in both.output
    # case-insensitive / kebab-normalized lookups
    assert runner.invoke(app, ["tag", "Shell"]).exit_code == 0


def test_tag_unknown(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["tag", "nope"])
    assert r.exit_code == 1


def test_add_new_tool_with_tags(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    monkeypatch.setenv("EDITOR", "true")
    r = runner.invoke(
        app,
        ["add", "fzf", "--category", "Search", "--desc", "fuzzy finder", "--tags", "search, fuzzy"],
    )
    assert r.exit_code == 0
    assert "**Tags:** search · fuzzy" in (repo.notes_dir / "fzf.md").read_text()


def test_add_tags_on_existing_errors(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    monkeypatch.setenv("EDITOR", "true")
    r = runner.invoke(app, ["add", "ssh", "--tags", "remote"])
    assert r.exit_code == 1


# --- prose search ---------------------------------------------------------


def test_find_prose_body(repo: Root):
    (repo.notes_dir / "paint.md").write_text(
        "# revere-pewter\n\nBenjamin Moore Revere Pewter HC-172.\n\n"
        "## Living room\n\n- two coats over primer\n"
    )
    # matches a body bullet only reachable via prose search
    res = notes.find([repo], ["coats"])
    assert len(res) == 1
    e = res[0]
    assert e.kind == "prose" and e.rank == 0
    assert e.command == "two coats over primer"  # leading "- " stripped
    assert e.section == "Living room"


def test_find_prose_via_title(repo: Root):
    # "pewter" lives only in the title; the body line carries it as context
    (repo.notes_dir / "paint.md").write_text("# revere-pewter\n\nBenjamin Moore, 2 coats.\n")
    res = notes.find([repo], ["pewter"])
    assert len(res) == 1 and res[0].kind == "prose"


def test_find_skips_fenced_and_headings(repo: Root):
    # prose search must ignore code-fence lines and heading text
    text = "# note\n\nbody line here.\n\n```bash\nsecret-cmd\n```\n"
    got = [txt for _, _, txt in notes.iter_prose(text)]
    assert got == ["body line here."]


# --- delete ---------------------------------------------------------------


def test_delete_categorized_empties(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["delete", "ssh", "-y"])
    assert r.exit_code == 0
    assert not (repo.notes_dir / "ssh.md").exists()
    # category had only ssh -> removed + unlinked from index
    assert not (repo.categories_dir / "network.md").exists()
    assert "network.md" not in repo.index.read_text()
    assert "[ssh]" not in repo.readme.read_text()  # README bullet gone


def test_delete_alias_rm(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["rm", "ssh", "-y"])
    assert r.exit_code == 0
    assert not (repo.notes_dir / "ssh.md").exists()


def test_delete_uncategorized(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["delete", "orphan", "-y"])
    assert r.exit_code == 0
    assert not (repo.notes_dir / "orphan.md").exists()
    # network category untouched
    assert (repo.categories_dir / "network.md").exists()


def test_delete_dry_run_writes_nothing(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    before = (repo.notes_dir / "ssh.md").read_text()
    r = runner.invoke(app, ["delete", "ssh", "--dry-run"])
    assert r.exit_code == 0 and "DRY-RUN" in r.output
    assert (repo.notes_dir / "ssh.md").read_text() == before
    assert (repo.categories_dir / "network.md").exists()


def test_delete_unknown(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    assert runner.invoke(app, ["delete", "nope", "-y"]).exit_code == 1


def test_delete_confirm_abort(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    r = runner.invoke(app, ["delete", "ssh"], input="n\n")
    assert r.exit_code == 1
    assert (repo.notes_dir / "ssh.md").exists()  # not deleted


# --- prose add + optional category ----------------------------------------


def test_add_prose_note(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    monkeypatch.setenv("EDITOR", "true")
    r = runner.invoke(app, ["add", "paint", "--prose", "--category", "Home", "--tags", "home"])
    assert r.exit_code == 0
    text = (repo.notes_dir / "paint.md").read_text()
    assert "**Tags:** home" in text
    assert "```bash" not in text  # prose: no shell scaffold
    assert capture.PROSE_BODY in text


def test_add_without_category_is_uncategorized(repo: Root, monkeypatch):
    monkeypatch.setenv("KB_ROOTS", f"{repo.label}={repo.path}")
    monkeypatch.setenv("EDITOR", "true")
    r = runner.invoke(app, ["add", "shower-idea", "--prose"])
    assert r.exit_code == 0
    assert (repo.notes_dir / "shower-idea.md").exists()
    # listed in README but in no category file
    assert "[shower-idea]" in repo.readme.read_text()
    cats = notes.list_categories(repo)
    assert notes.find_tool_category(repo, "shower-idea") is None
    assert "shower-idea" in notes.orphan_tools(repo, cats)


def test_write_new_note_prose_return_line(tmp_path):
    p = tmp_path / "x.md"
    land = capture.write_new_note(p, "x", "desc", tags=["a"], prose=True)
    assert p.read_text().splitlines()[land - 1] == capture.PROSE_BODY


def test_remove_readme_bullet(repo: Root):
    assert capture.remove_readme_bullet(repo, "ssh") is True
    assert "[ssh]" not in repo.readme.read_text()
    assert capture.remove_readme_bullet(repo, "ssh") is False  # already gone


def test_root_for():
    pub = Root("pub", Path("/tmp/pub"))
    priv = Root("private", Path("/tmp/private"))
    roots = [pub, priv]
    assert root_for(roots, "") is pub
    assert root_for(roots, "private") is priv
    assert root_for(roots, "priv") is priv
    assert root_for(roots, "nope") is None
