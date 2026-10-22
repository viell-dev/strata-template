# GitHub verification workflows

Workflow payloads for the [Rust library recipe](../rust-library/README.md). Merge checks run
its fast checks on every pull request's head commit. Release checks run all three stages as
separate jobs, only when a maintainer dispatches them. Keep their commands identical to the
adopting repository's `CONTRIBUTING.md` and `RELEASING.md`.

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `rust-library-merge-checks.yml.tmpl` | `.github/workflows/merge-checks.yml` | Filled, then owned | `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}` |
| `rust-library-release-checks.yml.tmpl` | `.github/workflows/release-checks.yml` | Filled, then owned | `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}`, `{{PROJECT_NAME}}` |

Use a Linux runner label such as `ubuntu-latest` and a reviewed checkout action pinned to its
full commit hash, such as `actions/checkout@<commit> # <tag>`. The
[Dependabot configuration](../../dependencies/README.md) proposes updates to that pin and its
version comment. `{{PROJECT_NAME}}` is the Cargo package
name. The `${{ … }}` expressions are GitHub syntax, not template placeholders. The runner needs
Git, Node.js for the chosen checkout action, curl, and a C linker. Each job installs rustup and
its required compiler; no cache is configured.

The workflows request only `contents: read`, discard checkout credentials, and receive no
publication secrets. Enable GitHub Actions in the adopting repository. These checks do not
publish packages, create tags, or merge changes.

## Running checks

A new push cancels the previous merge-check run for that pull request. Checks use the PR head,
so their result identifies the commit being reviewed rather than a temporary merge commit.

GitHub requires a `workflow_dispatch` workflow to exist on the default branch before it can be
[run manually](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).
Land the workflow first, then dispatch `release-checks.yml` on the release branch, for example:

```bash
gh workflow run release-checks.yml --ref release-0-1-3
```

Record the run's actual head SHA in the release PR. If that branch changes, rerun the gate on
the new commit. Never treat an older successful run as verification of a newer release commit.

## Verification

Validate the filled workflows on the adopting repository and runner. Check that each run uses
the intended SHA and that all documented stages pass before relying on its results.

The updated extracted-package all-targets and doctest commands have been checked locally; the
revised release workflow has not yet run on a GitHub runner.
