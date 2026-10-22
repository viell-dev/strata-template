# Contributing

This repository holds reusable starting points for other repositories. Propose a component or
variant when an actual repository benefits from it, and describe that use case and the
customization it needs. Keep independent concerns separate, and state dependencies, such as a
contribution policy that requires particular license files, in the component's README.

## Conventions

- Payloads end in `.tmpl`; everything else is this repository's own documentation.
- Placeholders use the `{{NAME}}` vocabulary in the [README](README.md). Add a name only when no
  existing one fits, and add it to that table.
- Every variant README has a file table with destination, ownership mode, and placeholders,
  followed by installation steps and verification.
- Concern READMEs list their variants. Guides under `docs/guides/` order the steps and link to the
  component READMEs rather than restating them.
- Wrap prose at 100 columns; leave code, tables, and long URLs intact.

## Checks before submitting

There is no tooling yet, so check by hand:

- Local documentation links resolve.
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
