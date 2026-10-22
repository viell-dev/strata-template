# MPL-2.0 with Rust clarification

MPL-2.0 file-level weak copyleft, a statement of intent that clarifies how the license applies to
ordinary Rust usage (linking, monomorphization, inlining, macro expansion, generated code), and an
MIT-0 grant for example material so that documentation snippets, `examples/`, integration tests,
and benchmarks can be copied without MPL obligations. The compilation and example-scope statements
are specific to Rust crates.

Use with [contributing/mpl-2.0-rust](../../contributing/mpl-2.0-rust/README.md): the clarification
links to `CONTRIBUTING.md`, and the contribution terms bind contributors to the clarification.
Install both at the repository root so their relative links resolve together.

## Files

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `LICENSE.tmpl` | `LICENSE` | Verbatim | None |
| `LICENSE-MIT-0.tmpl` | `LICENSE-MIT-0` | Filled | `{{YEAR}}`, `{{COPYRIGHT_HOLDER}}` |
| `LICENSE-CLARIFICATION.md.tmpl` | `LICENSE-CLARIFICATION.md` | Verbatim | None |
| `README-LICENSE.md.tmpl` | The `## License` section of `README.md` | Verbatim section | None |

`LICENSE` is Mozilla's MPL-2.0 text and `LICENSE-MIT-0` is the MIT-0 text. Nothing beyond the
MIT-0 notice line may be edited, so both keep matching their SPDX identifiers. The clarification
is edited upstream only: it is the text contributors endorse, and a local wording change would
make the adopter's contribution terms diverge from the published statement.

## Installation

1. Copy the three license files to the repository root, dropping `.tmpl`, and fill the MIT-0
   notice line.
2. Insert the README section payload into the crate README. Its wording is generic and links to
   the files above and to `CONTRIBUTING.md`.
3. Install the companion contribution variant.
4. In `Cargo.toml`, set `license = "MPL-2.0"`. Do not use `license-file`, and do not write a
   dual-license expression: the crate as a whole is MPL-2.0, and only the example material carries
   the MIT-0 grant. If the package uses an explicit `include` list, add:

   ```toml
   "CONTRIBUTING.md",
   "LICENSE",
   "LICENSE-CLARIFICATION.md",
   "LICENSE-MIT-0",
   "README.md",
   ```

## Verification

- **Example-material scope.** The MIT-0 grant mechanically covers fenced code blocks in Markdown
  and rustdoc and everything under `examples/`, `tests/`, and `benches/`. Confirm none of that
  contains third-party or differently licensed material; where it does, mark the file or block as
  the clarification allows ("except where a file or an individual fenced block expressly states
  otherwise").
- **Package contents.** `cargo package --list` must show every file the README and clarification
  link to. Follow the [Rust package checks](../../ci/rust-library/README.md#package): run
  `cargo package`, then `cargo test --all-targets --all-features` and
  `cargo test --doc --all-features` from the extracted copy in
  `target/package/<name>-<version>/`. This checks shipped targets, including benchmarks, and
  doctests separately.
- **Rendering.** Check the README section and its links in the adopting repository.
