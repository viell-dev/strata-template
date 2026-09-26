# Issue prompts

Individually selectable prompts in Forgejo Markdown front-matter form. Copy the chosen files into
`.forgejo/issue_template/`, dropping `.tmpl`. They need no labels and contain no placeholders.
Each is _owned_ after copying, so adapt the wording to the repository.

| Payload | Asks for | Suited to |
| --- | --- | --- |
| `bug-report.md.tmpl` | Version, environment, reproduction, expected and actual behavior | Any project; edit the environment question for the stack |
| `rust-library-bug.md.tmpl` | Crate version, compiler, OS and target, a Rust reproducer | Cargo libraries |
| `proposal.md.tmpl` | Problem or question, context, optional direction | Any project; keeps an unstructured question path |

Select one bug prompt, not both. Add stack-specific variants (browser and version for a web
project, editor host for an extension, runtime and deployment for a service) when such a project
exists, rather than asking Rust questions of everyone.

Forgejo also accepts YAML forms and the uppercase `ISSUE_TEMPLATE` directory; see the
[Forgejo template documentation](https://forgejo.org/docs/latest/user/repository/issue-pull-request-templates/).
These prompts have not been exercised on Codeberg. After landing them on the default branch, open
a test issue and check the form and the resulting issue.
