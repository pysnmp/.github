// Commit messages here follow the same convention as the library repositories,
// for one reason: this is where a contributor's first pull request to the
// organization often lands, and a habit picked up on a typo fix carries over to
// pysnmp, where the message is the input to the release rather than decoration.
//
// One file, two places. The commit-msg hook in .pre-commit-config.yaml checks a
// message as it is written; .github/workflows/commit-conventions.yml checks
// every commit in a pull request. Both read this config, so a message that
// passes locally passes in CI.
export default {
  extends: ["@commitlint/config-conventional"],
  rules: {
    // The same list the library repositories accept, restated here so the set
    // stays put if the shared preset ever widens it. Anything outside it is a
    // typo -- a "feature:" or "bugfix:" commit parses as no type at all, and
    // over in pysnmp that means it drops out of the release notes.
    "type-enum": [
      2,
      "always",
      [
        "build",
        "chore",
        "ci",
        "docs",
        "feat",
        "fix",
        "perf",
        "refactor",
        "revert",
        "style",
        "test",
      ],
    ],

    // Bodies are written by tools as often as by hand -- a dependabot body
    // carries compare links -- and those do not wrap to a column. Not worth
    // failing a commit over.
    "body-max-line-length": [0],
    "footer-max-line-length": [0],

    // The subject is prose and starts with whatever word it starts with --
    // "docs: PySNMP is two words on the profile" is not a style error. The type
    // stays lower case (type-case, from the shared preset), because that is
    // what semantic-release matches its release rules on elsewhere.
    "subject-case": [0],
  },
};
