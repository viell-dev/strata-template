# MIT-0 contribution policy

Companion to [license/mit-0](../../license/mit-0/README.md). Contributions are accepted under the
same MIT-0 terms, and contributors identify third-party material so its notices can be reviewed.

## Files

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `CONTRIBUTING.md.tmpl` | `CONTRIBUTING.md` | Filled; everything but the Licensing section owned | `{{PROJECT_NAME}}`, `{{REPO_URL}}`, `{{DEVELOPMENT}}` |
| `pull_request_template.md.tmpl` | `.github/pull_request_template.md` | Filled, optional | `{{REPO_URL}}` |

## Installation

1. Copy `CONTRIBUTING.md.tmpl`, fill the name and URL, and write the Development section: the
   tools the repository actually uses, style conventions, and how to check a change.
2. Rewrite the rest freely. A documentation hub will want to say which issues belong there and
   which belong in other repositories; a service will want deployment notes. Keep the Licensing
   section as written.
3. Optionally copy the PR prompt. It links to the contribution guide by absolute URL because
   relative links in PR bodies do not resolve reliably. The payload uses GitHub
   `blob/main`; adapt that path for another host.

Nothing here assumes Cargo or any particular stack.
