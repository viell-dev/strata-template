# Issue and pull request labels

A shared label catalog, so that every adopting repository classifies its work the same way. The
catalog holds each label's name, color, and description; this README explains when each one
applies and how to bring a repository's labels in line with it.

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `labels.json.tmpl` | `.github/labels.json` | Verbatim | None |

The copied file is the repository's record of its shared labels; the forge's live labels are kept
in sync with it. A repository may add labels for a distinction the catalog lacks, such as a
component name, and documents them where it keeps its contributor notes rather than in the copied
file, so that an update can replace that file. It does not redefine shared labels or create
synonyms for them.

## Groups

- **Type:** exactly one on every issue and pull request, naming the kind of work.
- **Status:** at most one, recording the current disposition. An untriaged item has none.
- **Needs:** what the maintainer has to do before the item can proceed. It can accompany a
  status.
- **Topics:** `Breaking Change`, `Soundness`, `Performance`, and `Experiment`, in any number,
  for concerns that cut across types.
- **Contributors:** `Good First Issue` and `Help Wanted`, only on accepted issues with a clear
  approach.

Target versions are milestones named after the version, such as `0.2.0`, not labels.

## Choosing a type

- `Type: Bug` when the code behaves incorrectly. When the behavior is right and the
  documentation describes it wrongly, the item is `Type: Documentation`.
- `Type: Enhancement` changes what an existing capability does or how it is used, including its
  API and performance. `Type: Feature` adds a capability that is useful on its own.
- `Type: Design` when the outcome is a decision or direction rather than a change. A concrete
  change that only needs one choice made keeps its own type and gains `Needs: Decision`.
- `Type: Testing` covers tests, benchmarks, Miri, fuzzing, and other verification.
  `Type: Maintenance` covers the rest of the upkeep around the code: dependencies, toolchains,
  CI, releases, and refactoring.
- `Type: Tracking` marks an index whose items are separate issues, such as a review report or a
  list of follow-up issues. It closes when its items are resolved. A checklist of small fixes
  tracked in the issue itself takes the type of that work.

## Status

- `Status: Confirmed` records a reproduced defect, with the evidence in the issue, or a request
  the maintainer has accepted. Only the maintainer accepts requests. It is not a commitment to
  deliver.
- `Status: Blocked` names and links what the item waits for. Waiting for the maintainer is
  `Needs: Decision` or `Needs: Review` instead.
- `Status: Needs Information` waits for the reporter; remove it when the answer arrives.
- `Status: Can't Reproduce`, `Status: Duplicate`, and `Status: Won't Do` accompany closing the
  item, with a comment that explains the outcome or links the canonical issue.

## Needs

`Needs: Decision` marks a choice that belongs to the maintainer: design, API, naming, scope, or
policy. State the decision needed, the options, and a recommendation. Once decided, record the
decision in the item and remove the label.

`Needs: Review` reflects that the maintainer aims to understand the code the project releases.
Agents may open pull requests from the maintainer's own account, where the forge cannot record the
maintainer's approval of their own pull request. Such a pull request carries `Needs: Review` from
the start and is not merged while it does:

1. The maintainer approves by saying so in a comment, or by instructing an agent to merge it.
   Requested changes keep the label.
2. An approval given outside the pull request, for example in an agent's working session, is
   recorded on the pull request by whoever acts on it before merging.
3. The label is removed once approval is recorded, and only then is the pull request merged.

Pull requests from other accounts use the forge's own reviews. Pull requests into an experimental
branch that will not be released as it stands do not need the label. On an issue, the label asks
the maintainer to read existing code or documents, such as code merged before this rule applied.

## Topics

- `Breaking Change` when the change requires a semver-incompatible release: a new major version,
  or a new minor version before 1.0.
- `Soundness` for `unsafe` code and memory safety: a wrong or missing safety argument, an API that
  lets safe code cause undefined behavior, or undefined behavior found by a tool such as Miri.
- `Performance` for speed, allocation, or memory use, whatever the type.
- `Experiment` for work on an experimental branch or proof of concept that is not mainline code.

## Applying the catalog

Copy `labels.json.tmpl` to `.github/labels.json`. The commands below use the GitHub CLI and `jq`,
run from the repository's checkout. On another forge, apply the same names, colors, and
descriptions through its interface.

A repository created on GitHub starts with GitHub's default labels. Rename those it has first,
so that existing issues and pull requests keep them:

| Default label | Rename to |
| --- | --- |
| `bug` | `Type: Bug` |
| `enhancement` | `Type: Enhancement` |
| `documentation` | `Type: Documentation` |
| `question` | `Type: Question` |
| `duplicate` | `Status: Duplicate` |
| `wontfix` | `Status: Won't Do` |
| `good first issue` | `Good First Issue` |
| `help wanted` | `Help Wanted` |

```bash
gh label edit bug --name "Type: Bug"
gh label edit "good first issue" --name "Good First Issue"
```

Then create the remaining labels and update the colors and descriptions of existing ones:

```bash
jq -r '.[] | [.name, .color, .description] | @tsv' .github/labels.json |
  while IFS=$'\t' read -r name color description; do
    gh label create "$name" --color "$color" --description "$description" --force
  done
```

List the labels the catalog does not define:

```bash
comm -23 <(gh label list --limit 1000 --json name --jq '.[].name' | sort) \
  <(jq -r '.[].name' .github/labels.json | sort)
```

Delete the leftovers, such as `invalid` and `accessibility`, or document them as the
repository's own. Deleting a label removes it from every item, so first check where it is used
with `gh issue list --label <name> --state all` and `gh pr list --label <name> --state all`.

The default labels are broader than the catalog's. Review existing items after renaming: an old
`enhancement` may be a feature, test, or design question, and an old `question` may be a pending
decision.

## Verification

- `.github/labels.json` is byte-identical to `labels.json.tmpl`.
- `gh label list` shows every catalog label with the catalog's color and description, and the
  leftover listing is empty or names only documented repository labels.
- Every open issue and pull request has exactly one `Type:` label and at most one `Status:`
  label.
