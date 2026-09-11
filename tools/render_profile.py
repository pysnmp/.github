#!/usr/bin/env python3
"""Render the project table in ``profile/README.md`` from ``projects.toml``.

``profile/README.md`` is the page GitHub shows on github.com/pysnmp. Its prose
is written by hand; the table of projects in the middle of it is generated,
between the two marker comments, so that adding a repository to the
organization is one edit to ``projects.toml`` rather than an edit here and a
second one that gets forgotten.

Usage::

    python tools/render_profile.py            # rewrite the table
    python tools/render_profile.py --check    # fail if it is out of date

CI runs the second form. See ``.github/workflows/ci.yml``.
"""

from __future__ import annotations

import argparse
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

#: Everything between these two lines is generated. They stay in the file.
BEGIN = "<!-- BEGIN PROJECTS -->"
END = "<!-- END PROJECTS -->"

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECTS = REPO_ROOT / "projects.toml"
PROFILE = REPO_ROOT / "profile" / "README.md"

HEADER = (
    "| Project | Install | Documentation | What it is |",
    "| --- | --- | --- | --- |",
)


@dataclass(frozen=True)
class Project:
    """One repository this organization maintains.

    Attributes
    ----------
    name
        The repository name, which is also how the project is spoken about.
    repo
        ``owner/name``, as it appears in a GitHub URL.
    summary
        One sentence saying what the project is. It becomes a table cell, so
        it has to read as one and cannot contain a newline.
    docs
        Where the published documentation lives.
    distribution
        The name on PyPI, or ``None`` for a repository that publishes no
        package.
    install
        What the Install cell should say, when a pip command is the wrong
        answer. The MIB distribution is served, unpacked or mounted rather
        than installed, and "--" undersells that.
    prerelease
        Whether the maintained line is still a release candidate, which makes
        the install command need ``--pre``. Nothing sets it today; it is kept
        because this organization cuts release candidates routinely and the
        table should say so while one is current.
    """

    name: str
    repo: str
    summary: str
    docs: str
    distribution: str | None = None
    install: str | None = None
    prerelease: bool = False

    @property
    def url(self) -> str:
        """The repository's page on GitHub."""
        return f"https://github.com/{self.repo}"

    @property
    def install_cell(self) -> str:
        """What the Install column says for this project."""
        if self.install:
            return self.install

        if not self.distribution:
            return "--"

        pre = "--pre " if self.prerelease else ""
        return f"`pip install {pre}{self.distribution}`"

    def row(self) -> str:
        """The project as one row of the generated Markdown table."""
        return (
            f"| [{self.name}]({self.url}) "
            f"| {self.install_cell} "
            f"| [docs]({self.docs}) "
            f"| {self.summary} |"
        )


def load_projects(path: Path = PROJECTS) -> list[Project]:
    """Read *path* and return the projects it declares, in file order."""
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return [Project(**entry) for entry in data["project"]]


def render_table(projects: list[Project]) -> str:
    """The Markdown table for *projects*, without the marker comments."""
    return "\n".join([*HEADER, *(project.row() for project in projects)])


def splice(document: str, table: str) -> str:
    """Return *document* with the region between the markers replaced.

    Raises
    ------
    ValueError
        If the markers are missing, out of order, or repeated. Rewriting a
        file whose generated region cannot be located unambiguously would
        silently drop the prose around it, so this stops instead.
    """
    # Exactly one of each. A second pair is the dangerous case rather than the
    # obviously broken one: rewriting the first and leaving the second would
    # publish a stale table, and `--check` would then pass on a profile that
    # contradicts itself, because the region it compares is already correct.
    if document.count(BEGIN) != 1 or document.count(END) != 1:
        raise ValueError(
            f"{PROFILE} must contain exactly one {BEGIN} and one {END}; "
            f"found {document.count(BEGIN)} and {document.count(END)}"
        )

    start = document.index(BEGIN)
    end = document.index(END)

    if end < start:
        raise ValueError(
            f"{PROFILE} must contain {BEGIN} before {END}; "
            "the generated table goes between them"
        )

    return f"{document[:start]}{BEGIN}\n{table}\n{document[end:]}"


def main(argv: list[str] | None = None) -> int:
    """Rewrite the profile, or check it, and return a process exit status."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit non-zero if the rendered table differs",
    )
    args = parser.parse_args(argv)

    current = PROFILE.read_text(encoding="utf-8")
    updated = splice(current, render_table(load_projects()))

    if current == updated:
        return 0

    if args.check:
        print(
            f"{PROFILE.relative_to(REPO_ROOT)} is out of date with "
            f"{PROJECTS.relative_to(REPO_ROOT)}; "
            "run `uv run python tools/render_profile.py` and commit the result.",
            file=sys.stderr,
        )
        return 1

    PROFILE.write_text(updated, encoding="utf-8")
    print(f"rewrote {PROFILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
