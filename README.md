# .github

Organization-wide defaults for [github.com/pysnmp](https://github.com/pysnmp).
Nothing here is a library; it is the text and configuration GitHub reads on
behalf of every other repository in the organization.

| Path | What GitHub does with it |
| --- | --- |
| [`profile/README.md`](profile/README.md) | The page shown on the organization's front page. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Linked from every new issue and pull request in a repository that has no copy of its own. |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | Same, and shown in each repository's community profile. |
| [`SECURITY.md`](SECURITY.md) | The "Report a vulnerability" text on every repository's Security tab. |
| [`SUPPORT.md`](SUPPORT.md) | Linked from the new-issue chooser. |
| [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE) | The issue forms offered by repositories with no templates of their own. |
| [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) | The pull request body a contributor starts from. |

A repository that ships its own copy of one of these files wins; the default is
only a fallback. So the text here is written to be true of every repository in
the organization, and anything specific to one of them belongs in that
repository instead.

## The profile page

[`profile/README.md`](profile/README.md) is prose, except for the table of
projects between the `<!-- BEGIN PROJECTS -->` and `<!-- END PROJECTS -->`
markers. That table is generated from [`projects.toml`](projects.toml):

```console
$ uv run python tools/render_profile.py            # rewrite it
$ uv run python tools/render_profile.py --check    # fail if it is stale
```

Adding a repository to the organization is therefore one edit to
`projects.toml` and one regeneration. The pre-commit hook and CI both run
`--check`, so the two cannot drift.

## Working on this repository

The toolchain is the one [pysnmp](https://github.com/pysnmp/pysnmp),
[pysmi](https://github.com/pysnmp/pysmi) and
[pyasn1](https://github.com/pysnmp/pyasn1) use:

```console
$ uv sync --locked
$ uv run --locked --group dev pytest
$ uv run ruff check . && uv run ruff format --check .
$ pre-commit install
```

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/);
see [CONTRIBUTING.md](CONTRIBUTING.md).
