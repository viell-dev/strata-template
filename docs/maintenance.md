# Maintenance

How adopted files relate to their source over time, and how this repository's own wording is
maintained. Nothing here requires tooling; the conventions are chosen so tooling can follow later.

## Recording a selection

For each adopted component, record enough to find its source again:

| Component | Variant | Source revision | Destination | Mode |
| --- | --- | --- | --- | --- |
| license | mpl-2.0-rust | `abc1234` | `LICENSE`, `LICENSE-MIT-0`, `LICENSE-CLARIFICATION.md` | Verbatim, MIT-0 filled |
| contributing | mpl-2.0-rust | `abc1234` | `CONTRIBUTING.md`, `.github/pull_request_template.md` | Filled; guide's Development section owned |
| contributing (alternative) | mit-0 | `abc1234` | `CONTRIBUTING.md`, optional `.github/pull_request_template.md` | Guide's Licensing section filled; remaining guide owned; prompt filled |
| issues | `rust-library-bug`, `proposal` | `abc1234` | `.github/ISSUE_TEMPLATE/` | Owned |
| labels | catalog | `abc1234` | `.github/labels.json` | Verbatim |
| dependencies | `dependabot-rust-library` | `abc1234` | `.github/dependabot.yml` | Owned |
| ci | rust-library | `abc1234` | `RELEASING.md` | Owned; project name initially substituted |
| ci | github | `abc1234` | `.github/workflows/merge-checks.yml`, `.github/workflows/release-checks.yml` | Owned; runner and action inputs initially substituted |
| security | github | `abc1234` | `SECURITY.md` | Filled; Supported versions and Handling reports owned |

These are examples of alternative selections, not a set to install together. Record inserted
sections, such as a README's License section, by file and heading as well as their source payload.
Use a full commit ID for durable records; the short revisions above are illustrative.

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
not drift. An unreplaced placeholder or an unrecorded change to material still declared verbatim
or filled is a defect worth fixing. If an adopter deliberately customizes such material, record
which file or section is now owned and review upstream changes manually for that part. This
changes the update contract, not any applicable license or contribution obligations; follow the
scope-change requirements below when those terms are affected.

## Tooling

The [catalog checker](../scripts/README.md) validates this repository's source and rendered
fixtures. No adoption/update tool exists yet. The intended one lives in this repository and applies
or updates selected components against a repository that is compatible with the template: its
adopted files are verbatim or filled copies, with owned material confined to the sections the file
tables mark as owned. Such a tool takes the recorded selection as input, renders filled files from
the recorded values, produces reviewable diffs for an explicit list of repositories, reports
leftover placeholders, and stops on conflicts. It never commits or publishes.

A repository customized beyond that, with recorded ownership changes or restructured files, is
outside the tool's automatic update scope and maintains its own checks. That is a valid state, not a
defect: the tool serves repositories that stay close to the template, and the others own their
divergence.


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

## This repository's adopted components

The template's own contribution guide is owned and retains its MIT-0 contribution terms. Its issue
and PR prompts were adopted from `1198eefdfcfea89e05fa8279d81c0be48bd1cfc4`:

| Source payload | Destination | Ownership and filled values |
| --- | --- | --- |
| `issues/bug-report.md.tmpl` | `.github/ISSUE_TEMPLATE/bug-report.md` | Owned; asks for template component/revision and rendered inputs |
| `issues/proposal.md.tmpl` | `.github/ISSUE_TEMPLATE/proposal.md` | Owned; initially copied unchanged |
| `issues/question.md.tmpl` | `.github/ISSUE_TEMPLATE/question.md` | Owned; initially copied unchanged |
| `contributing/mit-0/pull_request_template.md.tmpl` | `.github/pull_request_template.md` | Filled; `REPO_URL=https://github.com/viell-dev/strata-template` |

The issue chooser explicitly keeps blank issues available. Live labels use
`labels/labels.json.tmpl` directly; there is no separate `.github/labels.json` to synchronize.
The [catalog validator](../scripts/README.md), its CI workflow, and the pip/Actions Dependabot
configuration are repository-owned. This repository has no Cargo package or Rust toolchain to
update. Its validation workflow runs on PRs and `main` pushes with read-only permissions.
