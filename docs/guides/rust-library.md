# Guide: Rust library

An end-to-end checklist for a standalone Cargo library published to crates.io under MPL-2.0 with
the Rust clarification. Each step links to the component's own instructions, which stay
authoritative; this guide only orders them and adds the cross-cutting checks.

| Step | Component | Variant |
| --- | --- | --- |
| 1 | [license](../../license/README.md) | [mpl-2.0-rust](../../license/mpl-2.0-rust/README.md) |
| 2 | [contributing](../../contributing/README.md) | [mpl-2.0-rust](../../contributing/mpl-2.0-rust/README.md) |
| 3 | [issues](../../issues/README.md) | `rust-library-bug`, optionally `proposal` and `question` |
| 4 | [labels](../../labels/README.md) | catalog |
| 5 | [ci](../../ci/README.md) | [rust-library](../../ci/rust-library/README.md), optionally [github](../../ci/github/README.md) or [forgejo](../../ci/forgejo/README.md) |
| 6 | [dependencies](../../dependencies/README.md) | `dependabot-rust-library`, on GitHub |

## 1. License material

Copy `LICENSE`, `LICENSE-MIT-0`, and `LICENSE-CLARIFICATION.md` to the crate root and fill the
MIT-0 notice line. Insert the README section payload as the crate README's `## License` section.

In `Cargo.toml`, set `license = "MPL-2.0"`. Do not use `license-file` or a dual-license
expression; only the example material carries the MIT-0 grant. If the package uses an explicit
`include` list, add the three license documents, `CONTRIBUTING.md`, and `README.md`.

## 2. Contribution policy

Copy `CONTRIBUTING.md` to the crate root and the PR prompt to the location the host reads, such
as `.github/pull_request_template.md`. Fill the project name and repository URL, then write the
Development section. Cover at least:

- **Compilers.** `rust-version` in `Cargo.toml` declares the minimum supported Rust version for
  that release; `rust-toolchain.toml` selects the development compiler contributors get by
  default. The two differ, may differ from other crates, and change independently.
- **Lints and conventions.** Where lints are configured and any house rules, such as preferring
  `#[expect(lint, reason = "...")]` over `#[allow(lint)]`.
- **Tests, examples, and benchmarks.** Where each lives, where present, how to run them, and
  which ship in the package. Take verification commands from step 5; distinguish benchmark smoke
  checks under `cargo test --all-targets` from measurements with `cargo bench`, and link to any
  repository-owned methodology and results. Keep the separate doctest command.

The Licensing section stays as written.

## 3. Issue prompts

Copy `rust-library-bug.md.tmpl` and, if wanted, `proposal.md.tmpl` and `question.md.tmpl` into
the host's issue template directory, such as `.github/ISSUE_TEMPLATE/`, dropping `.tmpl`. Adjust
the wording to the crate; the files are owned after copying.

## 4. Labels

Copy the label catalog to `.github/labels.json`, rename GitHub's default labels, and sync the rest
as the labels README describes. Re-label existing issues and pull requests so that each has one
`Type:` label.

## 5. Verification

Copy `RELEASING.md.tmpl` to the crate root as `RELEASING.md` and fill the project name. Put the
fast checks from the Rust library recipe into the Development section or a repository-owned
script, and link to `RELEASING.md` using its repository URL so the link also works from the
published package. Add CI only when a runner exists for the repository. Copy the
[github](../../ci/github/README.md) or [forgejo](../../ci/forgejo/README.md) adapter's
`rust-library-` merge-check and release-check workflows, and keep their commands identical to
the contributor guide and `RELEASING.md`.

Choose any [optional hardening checks](../../ci/rust-library/README.md#optional-hardening-checks)
the crate needs. Record the verified Miri nightly, target prerequisites, commands, and execution
frequency in the owned Development section when adopting them; record results before claiming
coverage.

## 6. Dependency updates

On GitHub, copy the Dependabot configuration to `.github/dependabot.yml` and enable Dependabot
alerts and security updates. It relies on the merge checks from step 5 to test each proposed
update, and its README explains the MSRV check that Cargo updates still need before merging.

## 7. Check the result

- No placeholder remains in any copied file; the `${{ … }}` expressions in workflows are not
  placeholders. Relative links in `README.md`, `CONTRIBUTING.md`, and `LICENSE-CLARIFICATION.md`
  resolve, and the PR prompt's link renders in the forge's PR UI.
- `LICENSE` and `LICENSE-CLARIFICATION.md` are byte-identical to their sources; `LICENSE-MIT-0`
  differs only on the notice line.
- The example-material scope in `LICENSE-CLARIFICATION.md` (fenced code in Markdown and rustdoc,
  `examples/`, `tests/`, `benches/`) contains no third-party or differently licensed material, or
  each exception is marked as the clarification allows.
- `cargo package --list` shows every file the README and clarification link to, and not
  `RELEASING.md`. Run `cargo package`, then `cargo test --all-targets --all-features` and
  `cargo test --doc --all-features` inside `target/package/<name>-<version>/`.
- The live labels match `.github/labels.json`.
- On GitHub, the Dependabot page lists all three ecosystems without a configuration error.

## 8. Record the selection

Note the components, variants, source revision, and rendered values as described in
[Maintenance](../maintenance.md).
