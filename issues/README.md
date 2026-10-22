# Issue prompts

Individually selectable Markdown prompts with front matter for GitHub and Forgejo. Copy the chosen
files into `.github/ISSUE_TEMPLATE/`, dropping `.tmpl`. They contain no placeholders. Each is
_owned_ after copying, so adapt the wording to the repository.

The bug prompts apply `Type: Bug` and the question prompt `Type: Question`, from the
[label catalog](../labels/README.md). A forge ignores a label the repository does not define, so
adopt the catalog with them or remove the `labels` line. The proposal prompt applies no label:
whether a proposal is a feature, an enhancement, or a design question is decided during triage.

| Payload | Destination | Mode | Placeholders | Asks for |
| --- | --- | --- | --- | --- |
| `bug-report.md.tmpl` | `.github/ISSUE_TEMPLATE/bug-report.md` | Owned | None | Version, environment, reproduction, expected and actual behavior |
| `rust-library-bug.md.tmpl` | `.github/ISSUE_TEMPLATE/rust-library-bug.md` | Owned | None | Crate version, compiler, OS and target, a Rust reproducer |
| `proposal.md.tmpl` | `.github/ISSUE_TEMPLATE/proposal.md` | Owned | None | Problem, context, optional direction |
| `question.md.tmpl` | `.github/ISSUE_TEMPLATE/question.md` | Owned | None | The question and anything already tried |

Select one bug prompt, not both. Add stack-specific variants (browser and version for a web
project, editor host for an extension, runtime and deployment for a service) when such a project
exists, rather than asking Rust questions of everyone.

GitHub reads these prompts from the default branch; see the
[GitHub template documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates).
Forgejo also accepts this directory layout. The payloads have been checked for GitHub-compatible
front matter; preview the issue chooser after adopting them in a repository.

## Verification

- Preview the issue chooser after the files reach the default branch; confirm each selected prompt
  appears and its wording fits the repository.
- Confirm the bug and question prompts apply labels that exist in the destination repository.
- Keep a blank-issue path for reports that do not fit a prompt.
