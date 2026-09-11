# Contributing to pysnmp

This is the default for every repository under
[github.com/pysnmp](https://github.com/pysnmp): [pysnmp](https://github.com/pysnmp/pysnmp),
[pysmi](https://github.com/pysnmp/pysmi), [pyasn1](https://github.com/pysnmp/pyasn1)
and [mibs](https://github.com/pysnmp/mibs). They deliberately share a
toolchain, so what follows is true of all of them. Where a repository needs
something of its own it says so in its own `CONTRIBUTING.md` or README, and
that wins.

## Getting a checkout working

Every repository is managed with [uv](https://docs.astral.sh/uv/) and commits
its `uv.lock`. Install uv, then:

```console
$ git clone https://github.com/pysnmp/<repository>.git
$ cd <repository>
$ uv sync --locked
$ uv run --locked --group dev pytest
```

`--locked` is not optional in CI and is a good habit locally: it fails rather
than quietly resolving something different from what everyone else is running.
If a change genuinely needs a new dependency, edit `pyproject.toml`, run
`uv lock`, and commit the lockfile in the same commit.

Install the hooks once per checkout:

```console
$ pre-commit install
```

That installs both the `pre-commit` and the `commit-msg` hook -- the second one
checks the commit message format described below, at the point where rewording
it is still a retype rather than a rebase.

## Before you open a pull request

The same three things CI will run:

```console
$ uv run ruff check .
$ uv run ruff format --check .
$ uv run --locked --group dev pytest
```

Repositories that ship type annotations also run `uv run mypy`, and those with
a documentation build run:

```console
$ uv run --locked --group dev sphinx-build -n -W --keep-going -b html docs/source docs/build
```

`-W` makes warnings errors, so a broken cross-reference fails the build. That
is on purpose: the published site is the reference for a protocol library, and
a dead link in it costs someone an afternoon.

### What the linters are set to

ruff's configuration lives in each `pyproject.toml` and the rule set is shared
between repositories, docstrings (`D`, numpy convention) included. Do not
silence a rule inline to get a change through; either fix it, or make the case
for the exemption in `pyproject.toml`, where the next person can read the
reasoning. Several of the existing ignores are there because SNMP requires
something a general-purpose linter objects to -- MD5 and DES are specified by
RFC 3414, not chosen -- and each of those carries a comment saying so.

## Commit messages

Messages follow [Conventional Commits](https://www.conventionalcommits.org/).
This is enforced, and not as a matter of taste: semantic-release computes the
next version number and writes the release notes from the commit history, so a
message it cannot parse becomes a change that ships in no release note and
bumps no version.

```
<type>(<optional scope>): <subject>

<optional body>

<optional footer>
```

The accepted types are `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`,
`refactor`, `revert`, `style` and `test`. Of these:

- `feat` cuts a minor release, `fix` a patch release.
- A `BREAKING CHANGE:` footer, or a `!` after the type, cuts a major release.
- Everything else releases nothing on its own.

The subject is prose and may start with a capital; the type must be lower
case. `commitlint.config.mjs` in each repository is the authority, and both the
`commit-msg` hook and the **Commit conventions** CI check read that same file,
so a message that passes locally passes in CI.

## Branches and releases

This section describes the three repositories that publish a package --
[pysnmp](https://github.com/pysnmp/pysnmp), [pysmi](https://github.com/pysnmp/pysmi)
and [pyasn1](https://github.com/pysnmp/pyasn1). The two that publish nothing,
[.github](https://github.com/pysnmp/.github) and
[pysnmp.github.io](https://github.com/pysnmp/pysnmp.github.io), have only
`main`: there is no release to stage, so there is nothing for a second
long-lived branch to hold. Open pull requests against `main` there.

- `main` is the released line. `next` is where work integrates.
- Open your pull request against `next` unless you are fixing something that is
  broken on `main` right now.
- A release candidate is cut from `next` and a general release from `main`, both
  by dispatching the CI workflow by hand. No push releases anything.
- Dependabot targets `next` for the same reason: `main` only ever receives a
  merge from `next`, and a bump landing on `main` directly would make every
  promotion conflict.

Version numbers are never edited by hand. semantic-release writes them into
`pyproject.toml`, the package's `__init__.py` and `CHANGELOG.md` as part of the
release commit.

## Tests

A bug fix comes with a test that fails without it. A feature comes with tests
that cover the behaviour a user would rely on.

These are protocol libraries, so prefer a test that asserts against encoded
bytes or a decoded structure over one that asserts against a `repr`. Where
there is an RFC that says what the behaviour should be, cite it in the test's
docstring -- that is what makes the test reviewable years later.

## Python versions

The floor is Python 3.10 and the ceiling is whatever the CI matrix currently
runs. Do not use syntax newer than the floor, and check `requires-python` in
`pyproject.toml` rather than assuming; the answer is not the same in every
repository.

## Reporting things instead

- A security vulnerability goes through [SECURITY.md](SECURITY.md), privately,
  not into a public issue.
- A question about using the library goes to [SUPPORT.md](SUPPORT.md).
- Conduct concerns go to [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Licensing

Everything here is under the 2-clause BSD license in each repository's
`LICENSE.rst`. Opening a pull request means you are offering your contribution
under that license.
