# Contributing

This repository holds reusable starting points for other repositories. Propose a component or
variant when an actual repository benefits from it, and describe that use case and the
customization it needs. Keep independent concerns separate, and state dependencies, such as a
contribution policy that requires particular license files, in the component's README.

## Conventions

- Payloads end in `.tmpl`; other files document, configure, or validate this repository.
- Placeholders use the `{{NAME}}` vocabulary in the [README](README.md). Add a name only when no
  existing one fits, and add it to that table.
- Every variant README has a file table with destination, ownership mode, and placeholders,
  followed by installation steps and verification.
- Concern READMEs list their variants. Guides under `docs/guides/` order the steps and link to the
  component READMEs rather than restating them.
- Wrap prose at 100 columns; leave code, tables, and long URLs intact.

## Issues, pull requests, and labels

Use the bug, proposal, or question prompt, or a blank issue when none fits. For template defects,
include the source revision, selected component, rendered values relevant to the problem, and a
small reproduction.

Follow the [shared label catalog](labels/README.md). Give every triaged issue and pull request one
`Type:` label; proposals without an initial type receive one during triage. This repository's live
labels use `labels/labels.json.tmpl` directly as their source, without a redundant copied catalog.

Agent-authored PRs submitted from the maintainer's account carry `Needs: Review` and follow the
[catalog's approval procedure](labels/README.md#needs). That approval must be recorded before the
label is removed and the PR is merged. External-account PRs use the host's normal review process.

## Checks before submitting

Run the [catalog checks](scripts/README.md), including the validator's regression tests. CI runs
those commands with actionlint on pull requests and pushes to `main`. The checker covers local
Markdown links, rendered fixtures, license integrity, labels, and basic workflow invariants; its
README distinguishes optional actionlint coverage from runner execution.

Also review the checks that require judgment or an actual adopter/runner:

- Preview changed Markdown where presentation matters, and check external links separately from
  deterministic local checks.
- Each changed payload renders correctly: copy it to a temporary directory with representative
  values, confirm no placeholder remains (workflow `${{ … }}` expressions are not placeholders),
  and check its links relative to the intended destination.
- `LICENSE.tmpl` and `LICENSE-MIT-0.tmpl` still match their canonical texts, and the MIT-0 copies
  in both license variants are identical.
- The label catalog parses as JSON, each color is six lowercase hexadecimal digits, each
  description fits GitHub's 100-character limit, and the labels README covers every label.
- Executable recipes were run when their commands changed. Say which workflows have actually been
  exercised on a runner, and keep the verification status in `ci/forgejo/README.md` current.
- Changes to the MPL/Rust contribution terms or the clarification follow
  [Maintenance](docs/maintenance.md): wording fixes are free, scope changes need an effective
  revision.

## Licensing

Original contributions are accepted under this repository's [MIT-0](LICENSE) license. Material
copied from elsewhere keeps its licensing and provenance; identify the source and revision. The
downstream contribution terms inside payloads do not govern changes to this repository.
