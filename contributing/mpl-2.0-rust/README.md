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
| `pull_request_template.md.tmpl` | `.github/pull_request_template.md` | Filled | `{{REPO_URL}}` |

The Licensing section stays as written; it is the text the assent sentence refers to. The assent
sentence in the guide and in the PR prompt must have identical visible wording; the prompt adds
Markdown link syntax around `CONTRIBUTING.md`. Use `.github/` for GitHub;
Forgejo also reads this location. The repository URL makes the contribution link resolve from
the pull request body.

## Installation

1. Copy both payloads, dropping `.tmpl`, and fill the project name and repository URL. The PR
   prompt uses the GitHub `blob/main` path; adapt that path when adopting it on another host.
2. Write the Development section. For a Rust crate, cover:
   - the compilers: `rust-version` in `Cargo.toml` declares the minimum supported Rust version
     for that release, while `rust-toolchain.toml` selects the development compiler contributors
     get by default. They are set independently, per crate, with no fixed update cadence;
   - lint configuration and house rules;
   - test layout and the commands to run, taken from the
     [Rust library recipe](../../ci/rust-library/README.md).
3. Open or preview a pull request to confirm the prompt appears and its `CONTRIBUTING.md` link
   reaches the destination repository and branch in the forge's PR UI.

## Verification

- No placeholder remains, and the Development section describes the actual checks.
- Outside that owned section, the contribution guide matches the filled payload.
- The assent has the same visible wording in the guide and prompt, and the prompt's absolute link
  reaches the installed guide.
- `LICENSE`, `LICENSE-MIT-0`, and `LICENSE-CLARIFICATION.md` are installed and their links resolve.

## Maintenance

Contributors are bound to the version of the clarification in effect when their contribution is
accepted, so wording fixes roll out freely while substantive scope changes do not bind earlier
contributors retroactively. See [Maintenance](../../docs/maintenance.md) before changing the
Licensing section or the clarification upstream.
