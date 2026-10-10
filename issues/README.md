# Issue prompts

Individually selectable Markdown prompts with front matter for GitHub and Forgejo. Copy the chosen
files into `.github/ISSUE_TEMPLATE/`, dropping `.tmpl`. They need no labels and contain no
placeholders.
Each is _owned_ after copying, so adapt the wording to the repository.

| Payload | Asks for | Suited to |
| --- | --- | --- |
| `bug-report.md.tmpl` | Version, environment, reproduction, expected and actual behavior | Any project; edit the environment question for the stack |
| `rust-library-bug.md.tmpl` | Crate version, compiler, OS and target, a Rust reproducer | Cargo libraries |
| `proposal.md.tmpl` | Problem or question, context, optional direction | Any project; keeps an unstructured question path |

Select one bug prompt, not both. Add stack-specific variants (browser and version for a web
project, editor host for an extension, runtime and deployment for a service) when such a project
exists, rather than asking Rust questions of everyone.

GitHub reads these prompts from the default branch; see the
[GitHub template documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates).
Forgejo also accepts this directory layout. The payloads have been checked for GitHub-compatible
front matter; preview the issue chooser after adopting them in a repository.
