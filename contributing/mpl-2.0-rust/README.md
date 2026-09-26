# MPL/Rust contribution policy

Companion to [license/mpl-2.0-rust](../../license/mpl-2.0-rust/README.md). The policy is
inbound=outbound under MPL-2.0 with two further conditions: example material is dual-licensed
under MIT-0, and contributors endorse the statement of intent in `LICENSE-CLARIFICATION.md`,
including a non-assertion promise for the benefit of downstream users. Agreement is recorded by a
sentence in each pull request description, which the PR prompt pre-fills.

## Files

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `CONTRIBUTING.md.tmpl` | `CONTRIBUTING.md` | Filled; Development section owned | `{{PROJECT_NAME}}`, `{{REPO_URL}}`, `{{DEVELOPMENT}}` |
| `pull_request_template.md.tmpl` | `.forgejo/pull_request_template.md` | Verbatim | None |

The Licensing section stays as written; it is the text the assent sentence refers to. The assent
sentence in the guide and in the PR prompt must stay identical. Forgejo also reads the PR prompt
from `.gitea/`, `.github/`, or `docs/`; `.forgejo/` is the convention here.

## Installation

1. Copy both payloads, dropping `.tmpl`, and fill the project name and repository URL.
2. Write the Development section. For a Rust crate, cover:
   - the compilers: `rust-version` in `Cargo.toml` declares the minimum supported Rust version
     for that release, while `rust-toolchain.toml` selects the development compiler contributors
     get by default. They are set independently, per crate, with no fixed update cadence;
   - lint configuration and house rules;
   - test layout and the commands to run, taken from the
     [Rust library recipe](../../ci/rust-library/README.md).
3. Open or preview a pull request to confirm the prompt appears and its `CONTRIBUTING.md` link
   renders in the forge's PR UI. If the relative link does not resolve there, switch it to the
   absolute repository URL and treat the prompt as owned.

## Maintenance

Contributors are bound to the version of the clarification in effect when their contribution is
accepted, so wording fixes roll out freely while substantive scope changes do not bind earlier
contributors retroactively. See [Maintenance](../../docs/maintenance.md) before changing the
Licensing section or the clarification upstream.
