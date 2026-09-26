# License material

License texts and the licensing statements that accompany them. Contribution policies live in
[contributing/](../contributing/README.md): contribution wording depends on the selected license,
so it is chosen separately and must agree with the license variant.

| Variant | License | Suited to | Companion contribution variant |
| --- | --- | --- | --- |
| [mpl-2.0-rust/](mpl-2.0-rust/README.md) | MPL-2.0 with a statement of intent for Rust compilation and an MIT-0 grant for example material | Rust crates | [contributing/mpl-2.0-rust](../contributing/mpl-2.0-rust/README.md), required |
| [mit-0/](mit-0/README.md) | MIT-0 for the whole project | Documentation, examples, anything meant to be copied freely | [contributing/mit-0](../contributing/mit-0/README.md), optional |

Variant names describe their contents, not a preference. A project's implementation language does
not select its license. Review the project's actual requirements, such as a dependency with
copyleft terms or a wish for MIT/Apache-style permissiveness, and add a descriptively named
variant when a concrete project needs one.

## Rules for every variant

- License texts are _verbatim_ payloads. `LICENSE.tmpl` and `LICENSE-MIT-0.tmpl` must match the
  canonical texts behind their SPDX identifiers (`MPL-2.0`, `MIT-0`); only the MIT-0 notice line
  carries placeholders.
- A variant is self-contained: copying its payloads installs everything the license material
  itself links to. Links across variants point only at the matching contribution variant.
- A variant README has a file table with destination, mode, and placeholders for every payload,
  followed by installation steps and verification.
- The MIT-0 text appears in both variants; the copies are kept identical.
