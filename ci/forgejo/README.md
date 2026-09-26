# Forgejo verification workflow

`verify.yml.tmpl` connects a repository-owned check command to a Forgejo Actions runner.

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `verify.yml.tmpl` | `.forgejo/workflows/verify.yml` | Filled, then owned | `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}`, `{{CHECK_COMMAND}}` |

| Placeholder | Meaning |
| --- | --- |
| `{{RUNNER_LABEL}}` | Label served by a runner configured for this repository |
| `{{CHECKOUT_ACTION}}` | Reviewed, fully qualified checkout action reference pinned to a commit |
| `{{CHECK_COMMAND}}` | Repository-owned verification command, such as `./scripts/check.sh` |

The workflow triggers on pushes to `main` and on pull requests; adjust the branch filter as
needed. The runner environment must provide the project's tools and whatever runtime the chosen
checkout action requires. No action reference, image, or runner is chosen for you. For a multiline
check command, indent every line under `run: |`.

Before activation, configure isolation and pull-request authorization for that runner. Check jobs
should not receive publication credentials or unrelated host access. Exercise successful and
failing push and PR jobs before relying on their status or making them required checks.

The payload has been checked as rendered YAML; execution on a runner has not been verified. Its
event and template syntax follow the
[Forgejo Actions reference](https://forgejo.org/docs/latest/user/actions/reference/); validate it
against the actual Codeberg instance and selected runner when adopting it.
