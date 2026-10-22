# Maintenance

How adopted files relate to their source over time, and how this repository's own wording is
maintained. Nothing here requires tooling; the conventions are chosen so tooling can follow later.

## Recording a selection

For each adopted component, record enough to find its source again:

| Component | Variant | Source revision | Destination | Mode |
| --- | --- | --- | --- | --- |
| license | mpl-2.0-rust | `abc1234` | `LICENSE`, `LICENSE-MIT-0`, `LICENSE-CLARIFICATION.md` | Verbatim, MIT-0 filled |
| contributing | mpl-2.0-rust | `abc1234` | `CONTRIBUTING.md`, `.github/pull_request_template.md` | Filled; Development owned |
| issues | `rust-library-bug`, `proposal` | `abc1234` | `.github/ISSUE_TEMPLATE/` | Owned |
| labels | catalog | `abc1234` | `.github/labels.json` | Verbatim |
| dependencies | `dependabot-rust-library` | `abc1234` | `.github/dependabot.yml` | Owned |

Add the rendered placeholder values and any deliberate deviation from the source. Keep the note
wherever the repository keeps its maintainer notes; it does not need to be published. A
repository may instead encode the same facts directly in its own checks.

## Updating adopted files

Treat a new template revision as an available update, reviewed per repository:

1. Diff the selected sources between the recorded revision and the new one.
2. Apply the diff by mode: replace _verbatim_ files, re-render _filled_ files and diff them
   against the copy in place, and read the diff of _owned_ material for changes worth carrying
   over.
3. Rerun the repository's checks, then update the recorded revision.

Stop on conflicts rather than overwriting. A difference in an owned section is a local decision,
not drift. An unreplaced placeholder or a modified verbatim file is a defect worth fixing.

## Tooling

No tool exists yet. The intended one lives in this repository and applies or updates selected
components against a repository that is compatible with the template: its adopted files are
verbatim or filled copies, with owned material confined to the sections the file tables mark as
owned. Such a tool takes the recorded selection as input, renders filled files from the recorded
values, produces reviewable diffs for an explicit list of repositories, reports leftover
placeholders, and stops on conflicts. It never commits or publishes.

A repository customized beyond that, with edits to verbatim material or restructured files, is
outside the tool's scope and maintains its own checks. That is a valid state, not a defect: the
tool serves repositories that stay close to the template, and the others own their divergence.

## Maintaining the source wording

This repository is the canonical home of the wording; adopting repositories hold governing
snapshots. A change here reaches an adopter only when that adopter applies the update.

The contribution terms in `contributing/mpl-2.0-rust/` bind each contributor to the version of
`LICENSE-CLARIFICATION.md` in effect when their contribution is accepted. Wording fixes that do not
change scope are therefore harmless to roll out. Substantive scope changes do not retroactively
bind earlier contributors: an adopter applying one should note the effective revision and decide
whether earlier contributions need separate agreement.

License texts are never edited. `LICENSE.tmpl` files and `LICENSE-MIT-0.tmpl` must match the
canonical texts behind their SPDX identifiers, with only the notice-line placeholders varying. The
MIT-0 text appears in both license variants; keep the copies identical.
