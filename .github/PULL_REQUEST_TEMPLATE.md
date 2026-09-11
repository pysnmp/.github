<!--
The title of this pull request becomes a commit message on `next`, so it has to
parse as a Conventional Commit:

    fix(smi): resolve a symbol imported through two MIB modules
    feat: SHA-384 and SHA-512 USM authentication protocols
    docs: correct the transport target example in the quick start

Types: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test.
A `!` after the type, or a `BREAKING CHANGE:` footer, cuts a major release.
-->

## What this changes

<!-- One paragraph. What is different after this is merged, and why. -->

## Why

<!--
The reasoning, or a link to the issue carrying it. If this implements something
a standard specifies, cite it: "RFC 7860 section 4.2.1".
-->

Fixes #

## How it was checked

<!-- Delete what does not apply; add what is missing. -->

- [ ] `uv run --locked --group dev pytest` passes
- [ ] `uv run ruff check .` and `uv run ruff format --check .` pass
- [ ] New or changed behaviour is covered by a test that fails without this change
- [ ] Documentation updated, and the docs build still passes with `-W`
- [ ] Tested against a real agent or device (say which)

## Notes for the reviewer

<!--
Anything that would otherwise be asked in review: a decision you were unsure
about, a case deliberately left out, a thing that looks wrong and is not.
-->
