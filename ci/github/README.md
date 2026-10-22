# GitHub verification workflows

Workflow payloads that run an adopting repository's checks on GitHub Actions. Choose the generic
merge-check adapter for an owned command, or the pair for the
[Rust library recipe](../rust-library/README.md). All merge checks run on the pull request's head
commit; the Rust release checks run all three stages as separate jobs on manual dispatch. Keep
the commands identical to the adopting repository's contributor and release instructions.

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `merge-checks.yml.tmpl` | `.github/workflows/merge-checks.yml` | Owned | `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}`, `{{CHECK_COMMAND}}` |
| `rust-library-merge-checks.yml.tmpl` | `.github/workflows/merge-checks.yml` | Owned | `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}` |
| `rust-library-release-checks.yml.tmpl` | `.github/workflows/release-checks.yml` | Owned | `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}`, `{{PROJECT_NAME}}` |

## Generic repository checks

Copy `merge-checks.yml.tmpl` when the repository has its own verification command, for example
`python3 scripts/check.py`. Fill the runner label, a reviewed full-SHA checkout action reference,
and `{{CHECK_COMMAND}}`. For a multiline command, indent every substituted line to the same level
as the original placeholder under `run: |`.

The runner needs Bash, Git, and the Node.js version required by the checkout action. The runner
image or owned command supplies every other tool; this adapter installs no language toolchain.
Its explicit Bash shell fails on pipeline errors. The command's exit status determines the check
result, and a new push cancels the older run for that PR. Adjust the owned timeout if needed.

Choose one merge-check payload for a destination workflow, not both. See the
[documentation guide](../../docs/guides/documentation.md) for one non-Rust use case.

## Rust library checks

The following setup applies to the `rust-library-` pair.

Use a Linux runner label such as `ubuntu-latest` and a reviewed checkout action pinned to its
full commit hash. Substitute only `actions/checkout@<commit>` for `{{CHECKOUT_ACTION}}`;
put an optional version comment outside the payload's quotes:

```yaml
uses: "actions/checkout@<full-commit-hash>" # <tag>
```

The [Dependabot configuration](../../dependencies/README.md) proposes updates to that pin and its
version comment. `{{PROJECT_NAME}}` is the Cargo package
name. The `${{ … }}` expressions are GitHub syntax, not template placeholders. The runner needs
Bash, Git, Node.js for the chosen checkout action, curl, and a C linker. Each job installs rustup and
its required compiler; no cache is configured.

Apply the recipe's [lockfile choice](../rust-library/README.md#lockfile-choices) consistently in
these owned workflows and the local checks. The payloads do not require a tracked lockfile or add
`--locked` automatically.

The workflows request only `contents: read`, discard checkout credentials, and receive no
publication secrets. Enable GitHub Actions in the adopting repository. These checks do not
publish packages, create tags, or merge changes.

The workflows explicitly select Bash so a failing command in a pipeline fails the step, including
an unsuccessful rustup download. Runner provisioning must make Bash available.

### Rustup bootstrap

The payloads deliberately use Rust's
[standard Unix installer](https://rust-lang.github.io/rustup/installation/other.html) over HTTPS.
The bootstrap script and installer are not pinned; they are trusted upstream inputs even when
the checkout action and compiler version are pinned. This choice avoids maintaining a separate
installer version and checksum in the templates, but does not provide a frozen build environment.
An adopter that needs a pinned bootstrap can use the documented versioned `rustup-init` download
and verify a reviewed checksum in its owned workflows. Keep the permission and secret limits
above in either case; those limits do not remove the need to trust the installer.

## Release metadata

The Rust release workflow also requires Python 3 for its standard-library JSON parser. It uses
`cargo metadata --no-deps --format-version 1` to read the standalone root package's declared
minimum compiler, package version, and target directory, independent of TOML formatting. The MSRV
job first installs the development compiler so Cargo can read the manifest, then installs and
tests with exactly the declared minimum. A missing `rust-version` fails explicitly.

The package job selects the exact extracted `<name>-<version>` directory reported by Cargo,
including a configured target directory; older package extracts do not affect selection.
`{{PROJECT_NAME}}` must match the root package name. Multi-package and virtual workspaces need an
adopter-owned workflow with explicit package selection; this adapter fails rather than choosing
an arbitrary workspace member.

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

GitHub's [Rebase and merge](https://docs.github.com/en/pull-requests/reference/pull-request-merges)
creates new commit SHAs. After merging a release PR, dispatch the gate on the resulting `main`
commit and verify the run's head SHA before tagging. If `main` advances before dispatch, select a
branch at the intended release commit instead. Follow the release procedure's final-commit check;
a successful run on the earlier PR head is not enough.

## Verification

Validate the filled workflows on the adopting repository and runner. Check that each run uses
the intended SHA and that all documented stages pass before relying on its results.

The generic adapter's rendered command has been checked locally with a multiline success case,
a failing command, and a failing pipeline. Its event and cancellation behavior has not yet been
exercised on a GitHub runner.

Metadata selection, extracted-package tests, and fail-fast download behavior have been checked
locally with positive and negative fixtures. The revised workflow has not yet run on a GitHub
runner; local command checks do not establish event or runner behavior.
