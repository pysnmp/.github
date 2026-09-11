"""Checks on the renderer that keeps ``profile/README.md`` in step with TOML.

The thing worth testing here is not the Markdown -- it is that a malformed or
missing marker pair stops the run instead of eating the prose around it, and
that ``--check`` actually fails when the committed profile is stale. CI depends
on the second one to notice a project added to ``projects.toml`` and never
rendered.
"""

import pytest
import render_profile
from render_profile import BEGIN, END, Project, load_projects, render_table, splice

DOCUMENT = f"before\n\n{BEGIN}\nstale\n{END}\n\nafter\n"


def project(**overrides) -> Project:
    """A project with plausible fields, overridden per test."""
    fields = {
        "name": "pysnmp",
        "repo": "pysnmp/pysnmp",
        "summary": "SNMP engine.",
        "docs": "https://pysnmp.github.io/pysnmp/",
        "distribution": "pysnmplib",
    }
    return Project(**{**fields, **overrides})


def test_row_links_repo_and_names_the_distribution():
    """A packaged project gets a pip command a reader can copy."""
    row = project().row()

    assert "[pysnmp](https://github.com/pysnmp/pysnmp)" in row
    assert "`pip install pysnmplib`" in row


def test_a_prerelease_project_installs_with_pre():
    """Without --pre, pip resolves the last GA -- not what the site documents."""
    assert project(prerelease=True).install_cell == "`pip install --pre pysnmplib`"


def test_a_released_project_installs_without_pre():
    """--pre on a GA line would opt a reader into prereleases for no reason."""
    assert project().install_cell == "`pip install pysnmplib`"


def test_an_explicit_install_note_wins_over_the_pip_command():
    """The MIB distribution is installable, just not by pip; "--" undersells it."""
    assert project(install="live over HTTPS, or installed locally").install_cell == (
        "live over HTTPS, or installed locally"
    )


def test_row_of_an_unpackaged_project_has_no_pip_command():
    """The MIB archive is a website; offering to pip install it would lie."""
    row = project(name="mibs", repo="pysnmp/mibs", distribution=None).row()

    assert "pip install" not in row
    assert "| -- |" in row


def test_table_has_a_row_per_project_under_one_header():
    """The header is written once, whatever the projects are."""
    lines = render_table(
        [project(), project(name="pysmi", repo="pysnmp/pysmi")]
    ).splitlines()

    assert len(lines) == 4
    assert [line.startswith("| ---") for line in lines] == [False, True, False, False]


def test_splice_replaces_only_the_marked_region():
    """Prose on either side of the markers survives a rewrite."""
    spliced = splice(DOCUMENT, "TABLE")

    assert spliced == f"before\n\n{BEGIN}\nTABLE\n{END}\n\nafter\n"


def test_splice_is_idempotent():
    """Rendering twice is rendering once, which is what --check relies on."""
    once = splice(DOCUMENT, "TABLE")

    assert splice(once, "TABLE") == once


@pytest.mark.parametrize(
    "document",
    [
        "no markers at all",
        f"{BEGIN}\nunterminated\n",
        f"{END}\nbackwards\n{BEGIN}\n",
        f"{DOCUMENT}{DOCUMENT}",
        f"{BEGIN}\n{BEGIN}\nstale\n{END}\n",
    ],
    ids=["absent", "unterminated", "out-of-order", "two-pairs", "two-begins"],
)
def test_splice_refuses_a_document_it_cannot_locate_the_region_in(document):
    """Better to fail than to rewrite a file and drop what was around it."""
    with pytest.raises(ValueError, match="must contain"):
        splice(document, "TABLE")


def test_a_second_marker_pair_is_refused_rather_than_left_stale():
    """The case that would otherwise pass --check while publishing a stale table.

    Splicing only the first pair leaves the second one holding whatever it
    held before, and the next --check compares the region it already fixed and
    reports success. Refusing outright is the only answer that cannot lie.
    """
    with pytest.raises(ValueError, match="exactly one"):
        splice(f"{DOCUMENT}{DOCUMENT}", "TABLE")


def test_committed_projects_file_parses_and_is_not_empty():
    """projects.toml is read by CI; a typo in it should fail here first."""
    projects = load_projects()

    assert projects
    assert all(p.summary.endswith(".") for p in projects)
    assert all(p.docs.startswith("https://") for p in projects)


def test_committed_profile_is_up_to_date():
    """The same assertion `--check` makes, so `pytest` alone catches drift."""
    assert render_profile.main(["--check"]) == 0
