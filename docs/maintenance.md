# Maintenance

Adopting repositories maintain their own copies. A maintainer or agent can compare the relevant
template revisions and carry over useful changes; there is no planned adoption/update tool.

## Recording a selection

Keep a short note identifying the selected components and their source revision, using a full
commit ID or a link pinned to it. Record important local choices and any destination that would
otherwise be hard to find. For example, a note can say that the MPL/Rust license and contribution
components came from one revision, while the Development section and CI commands are maintained
locally. Record different revisions when components were adopted separately.

The note can live in existing maintainer documentation or the adoption commit. There is no required
format, manifest, or inventory of every inserted section. Record substituted values when they are
not evident in the adopted copy and would help a later update.

## Updating adopted files

Treat a new template revision as an available update, reviewed per repository:

1. Read the changes to the selected components since the recorded revision.
2. Review replacements for _verbatim_ files and substituted _filled_ text. For _owned_ material,
   adapt only the changes that help the repository, preserving its local decisions.
3. Review the resulting diff and run the repository's checks. Record which updates were applied;
   do not advance a component's revision just because unrelated components changed.

Resolve conflicts with the local intent in mind rather than overwriting changes. A newer template
revision does not by itself make an adopter out of date. Unfilled placeholders and accidental
changes to canonical text still need correction. When ordinary instructions are deliberately
adapted, note that they are now owned. This does not change license or contribution obligations;
follow the scope-change requirements below when those terms are affected.

## Source validation

The [catalog checker](../scripts/README.md), its tests, and required CI validate this repository's
source and representative rendered copies. They do not inspect adopters or enforce synchronization.
Their Python dependencies stay here; copying a component does not copy the validation toolchain.
Executable workflow payloads document their own runner requirements separately.

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

The owned [security policy](../SECURITY.md) follows the `security/github` component at
`1d79a775f4186fb8f12bebec7a37e56d5727dca7`. Its wording was adapted for template defects, fixes on
`main`, and the maintainer's discretionary report handling, as agreed in
[issue #31](https://github.com/viell-dev/strata-template/issues/31#issuecomment-6362723540).

The issue chooser explicitly keeps blank issues available. Live labels use
`labels/labels.json.tmpl` directly; there is no separate `.github/labels.json` to synchronize.
The [catalog validator](../scripts/README.md), its CI workflow, and the pip/Actions Dependabot
configuration are repository-owned. This repository has no Cargo package or Rust toolchain to
update. Its validation workflow runs on PRs and `main` pushes with read-only permissions.
