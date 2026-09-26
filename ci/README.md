# Verification and CI

Two kinds of component, kept separate: _recipes_ say what a repository verifies, and _adapters_
connect a repository-owned check command to a runner. The adopting repository owns its commands
and runtime requirements; an adapter only calls them.

## Recipes

What a repository verifies. Each is a documented command set for one kind of project:

- [rust-library/](rust-library/README.md): standalone Cargo libraries, in three stages (fast
  checks, MSRV check, release gate), with a release procedure payload that orders them around a
  tag and a publication and keeps a record of what was tested.
- [documentation/](documentation/README.md): an outline for Markdown repositories and sites,
  from which a repository picks the checks its formats need.

## Adapters

How the repository's check command reaches a runner:

- [forgejo/](forgejo/README.md): a Forgejo Actions workflow with explicit inputs for the runner
  label, checkout action, and check command.

Recipes are documentation, not scripts. Put the applicable commands into the repository's
contributor guide or its own check script, so they run identically with and without CI. Recipes
end at verification and never publish anything; publication credentials stay out of check jobs.

TypeScript, Python, editor extensions, websites, containers, and mixed repositories will need
their own recipes once a project establishes its package manager, supported runtime, and
build/test commands. There is no universal toolchain.
