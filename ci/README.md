# Verification and CI

Two kinds of component, kept separate: _recipes_ say what a repository verifies, and _adapters_
run those checks on a runner. The adopting repository owns its commands and runtime
requirements; an adapter only runs them.

## Recipes

What a repository verifies. Each is a documented command set for one kind of project:

- [rust-library/](rust-library/README.md): standalone Cargo libraries, in three stages (fast
  checks, MSRV check, package check), and a release procedure that runs them on the release
  commit, then tags and publishes.
- [documentation/](documentation/README.md): an outline for Markdown repositories and sites,
  from which a repository picks the checks its formats need.

## Adapters

How the repository's checks reach a runner:

- [github/](github/README.md): GitHub Actions merge checks for an owned command, plus a Rust
  library pair with fast merge checks and manually dispatched release checks.
- [forgejo/](forgejo/README.md): Forgejo Actions workflows for merge checks on every pull request
  and manually dispatched release checks, including a pair for the rust-library recipe.

Recipes are documentation, not scripts. Put the applicable commands into the repository's
contributor guide or its own check script, so they run identically with and without CI. A
workflow either calls that script or repeats the documented commands; keep a repeated copy
identical to the documentation.
Verification commands do not publish; publication credentials stay out of check jobs. The Rust
release procedure documents manual publication separately.

TypeScript, Python, editor extensions, websites, containers, and mixed repositories will need
their own recipes once a project establishes its package manager, supported runtime, and
build/test commands. There is no universal toolchain.
