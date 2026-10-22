# Forgejo verification workflows

Workflow payloads that run a repository's checks on a Forgejo Actions runner. They come in two
kinds:

- **Merge checks** run automatically on every pull request: the checks a change passes before it
  is merged.
- **Release checks** run only when a maintainer dispatches them: the slower checks a release
  needs on the commit to be tagged.

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `merge-checks.yml.tmpl` | `.forgejo/workflows/merge-checks.yml` | Owned | `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}`, `{{CHECK_COMMAND}}` |
| `rust-library-merge-checks.yml.tmpl` | `.forgejo/workflows/merge-checks.yml` | Owned | `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}` |
| `rust-library-release-checks.yml.tmpl` | `.forgejo/workflows/release-checks.yml` | Owned | `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}`, `{{PROJECT_NAME}}` |

A crate that follows the [rust-library](../rust-library/README.md) recipe takes the
`rust-library-` pair: its merge checks are the recipe's fast checks, and its release checks run
the recipe's three stages as separate jobs. The pair repeats the recipe's commands rather than
calling a script, so keep each workflow identical to the contributor guide and `RELEASING.md`
when either changes. Any other repository takes `merge-checks.yml.tmpl`, which runs one
repository-owned check command; for a multiline command, indent every line under `run: |`.

Apply the recipe's [lockfile choice](../rust-library/README.md#lockfile-choices) consistently in
these owned workflows and the local checks. The payloads do not require a tracked lockfile or add
`--locked` automatically.

| Placeholder | Meaning |
| --- | --- |
| `{{RUNNER_LABEL}}` | Label served by a runner configured for this repository |
| `{{CHECKOUT_ACTION}}` | Reviewed, fully qualified checkout action reference pinned to a commit |
| `{{CHECK_COMMAND}}` | Repository-owned verification command, such as `./scripts/check.sh` |
| `{{PROJECT_NAME}}` | The Cargo package name, which locates the extracted package |

Substitute only the checkout action reference for `{{CHECKOUT_ACTION}}`. An optional version
comment belongs after the closing YAML quote, not inside the placeholder value. For a multiline
`{{CHECK_COMMAND}}`, indent every substituted line to the same level as the original placeholder.

The `${{ … }}` expressions in the payloads are Forgejo syntax, not placeholders; keep them.

## Runner and repository setup

No runner, label, image, or action reference is chosen for you. The job image must provide
Node.js and Git for the checkout action. The `rust-library-` payloads also need curl and a C
linker: they install rustup in each job, then take the development compiler from
`rust-toolchain.toml` and the minimum from `rust-version` in `Cargo.toml`. A Debian-based Node.js
image such as `node:24-bookworm` provides all of these. For `merge-checks.yml.tmpl`, the image or
the check command must provide the project's tools. Nothing is cached, so each job downloads its
compilers.

Before relying on the workflows, enable Actions in the repository settings and configure the
runner's isolation. Check jobs should not receive publication credentials or unrelated host
access. Forgejo holds workflows from fork pull requests by untrusted authors until a maintainer
approves them.

### Rustup bootstrap

The Rust payloads deliberately use Rust's
[standard Unix installer](https://rust-lang.github.io/rustup/installation/other.html) over HTTPS.
The bootstrap script and installer are not pinned; they are trusted upstream inputs even when
the checkout action and compiler version are pinned. This choice avoids maintaining a separate
installer version and checksum in the templates, but does not provide a frozen build environment.
An adopter that needs a pinned bootstrap can use the documented versioned `rustup-init` download
and verify a reviewed checksum in its owned workflows. Keep the runner isolation and credential
limits above in either case; those limits do not remove the need to trust the installer.

## Behavior

- **Dispatching release checks.** Run them from the repository's Actions tab, or with the API,
  for example `fj actions dispatch release-checks.yml <branch>`. Forgejo reads the workflow from
  the ref being run, so a branch can use it only once it contains the file. The same applies to
  pull requests: a branch from before the workflow was added gets no merge checks.
- **Runner offline.** Jobs wait, and the pull request shows a pending check, until a runner with
  the label connects; they then run without intervention. A job that waits longer than the
  instance's abandoned-job timeout (24 hours by default) is cancelled, and a runner that
  disappears mid-job fails it after about ten minutes. Rerun a finished run from its page with
  "Re-run all jobs", or a single job with its rerun icon; this needs write access and the web UI.
- **New pushes.** A new push to a pull request cancels its older merge-check run. The cancelled
  run marks its commit with a failed status ("Has been cancelled"). The pull request shows only
  its head commit, but a superseded commit merged as it is keeps that status in the history.
- **Required checks.** A cancelled or abandoned run reports as a failure, and a check that never
  ran blocks a merge that requires it. While a runner is not always online, keep merge checks
  informational rather than required.

## Verification status

The `rust-library-` pair before the extracted-package all-targets change ran on Codeberg
(Forgejo 16.0-dev) with Forgejo Runner 13.2.0 and
`node:24-bookworm` jobs, adopted in strata-reader: passing runs of both workflows, an
intentionally failing commit that failed each release-check job at its own stage, merge checks on
a pull request, and a run cancelled by a newer push. `merge-checks.yml.tmpl` shares their trigger
and concurrency settings but has not itself run. Event and expression syntax follow the
[Forgejo Actions reference](https://forgejo.org/docs/latest/user/actions/reference/); validate a
workflow against the actual instance and runner when adopting it.

The updated extracted-package commands have been checked locally; the revised release workflow
has not yet run on a Forgejo runner.
