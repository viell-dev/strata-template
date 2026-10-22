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
full commit hash. Substitute only `actions/checkout@<commit>` for `{{CHECKOUT_ACTION}}`;
put an optional version comment outside the payload's quotes:

```yaml
uses: "actions/checkout@<full-commit-hash>" # <tag>
```

The [Dependabot configuration](../../dependencies/README.md) proposes updates to that pin and its
version comment. `{{PROJECT_NAME}}` is the Cargo package
name. The `${{ … }}` expressions are GitHub syntax, not template placeholders. The runner needs
Git, Node.js for the chosen checkout action, curl, and a C linker. Each job installs rustup and
its required compiler; no cache is configured.

Apply the recipe's [lockfile choice](../rust-library/README.md#lockfile-choices) consistently in
these owned workflows and the local checks. The payloads do not require a tracked lockfile or add
`--locked` automatically.

The workflows request only `contents: read`, discard checkout credentials, and receive no
publication secrets. Enable GitHub Actions in the adopting repository. These checks do not
publish packages, create tags, or merge changes.

### Rustup bootstrap

The payloads deliberately use Rust's
[standard Unix installer](https://rust-lang.github.io/rustup/installation/other.html) over HTTPS.
The bootstrap script and installer are not pinned; they are trusted upstream inputs even when
the checkout action and compiler version are pinned. This choice avoids maintaining a separate
installer version and checksum in the templates, but does not provide a frozen build environment.
An adopter that needs a pinned bootstrap can use the documented versioned `rustup-init` download
and verify a reviewed checksum in its owned workflows. Keep the permission and secret limits
above in either case; those limits do not remove the need to trust the installer.

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
