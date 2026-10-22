# Dependency updates

Configuration that has the forge propose dependency updates as pull requests, which then pass the
repository's merge checks and the maintainer's review like any other change. Dependabot is
GitHub's updater; add a variant for another forge's updater, such as Renovate, when a repository
hosted there needs one.

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `dependabot-rust-library.yml.tmpl` | `.github/dependabot.yml` | Owned | None |

The payload labels its pull requests `Type: Maintenance` from the
[label catalog](../labels/README.md). Dependabot ignores a label the repository does not define,
and an explicit `labels` list also stops it from creating its default `dependencies` and
ecosystem labels, so adopt the catalog first or change the list.

## Rust library

`dependabot-rust-library.yml.tmpl` checks three ecosystems once a month:

- **Cargo**, for the crate's dependencies of every kind. Minor and patch updates arrive together
  in one pull request; each major update gets its own. With a tracked `Cargo.lock`, pull requests
  also move locked versions within the declared requirements. Without one, they change only
  requirements in `Cargo.toml`, when a release falls outside them.
- **Rust toolchain**, for the development compiler that `rust-toolchain.toml` pins. A pull
  request moves a versioned `channel`, such as `1.98.1`, to the newest stable release; a bare
  `stable` channel has nothing to update. The checks in that pull request then run on the new
  compiler.
- **GitHub Actions**, for the actions in `.github/workflows/`, in one pull request. An action
  pinned to a commit hash is updated to the new release's hash, and a version comment on the same
  line is updated with it.

A seven-day cooldown keeps a release out of version updates until it is a week old, so that a
broken or compromised release is more likely to be yanked before it is proposed. Security updates
are not delayed.

Dependabot does not read `rust-version`. A Cargo update can require a newer compiler than the
crate's declared minimum, and the merge checks, which use the development compiler, will not
notice. Before merging a Cargo update, run the MSRV stage of the
[Rust library recipe](../ci/rust-library/README.md), for example by dispatching the release
checks on the pull request's branch. To keep a dependency on an older version, add an `ignore`
entry with a comment that says why.

A new compiler can bring lints and deprecations that the `-D warnings` checks turn into
failures, so a toolchain pull request may fail until the code changes. Fix the code in a separate
pull request, then comment `@dependabot rebase` on the toolchain pull request so that its checks
run again on top of the fix. Pushing the fix to Dependabot's branch also works, but Dependabot
stops rebasing a pull request once someone else has pushed to it. The new pin changes neither
`rust-version` nor the compiler that users of the crate need; contributors' rustup installs the
new compiler on their next build in the repository.

Dependabot's pull requests come from its own account, so the forge's own review applies to them;
they do not need `Needs: Review`.

## Applying the configuration

1. Copy the payload to `.github/dependabot.yml`. Change the schedule, groups, or labels if the
   repository needs to; the file is owned after copying.
2. Enable Dependabot alerts and security updates in the repository's settings, or with the
   GitHub CLI:

   ```bash
   gh api --method PUT repos/<owner>/<repo>/vulnerability-alerts
   gh api --method PUT repos/<owner>/<repo>/automated-security-fixes
   ```

3. Land the file on the default branch. Dependabot reads it only from there.

See the [Dependabot options reference](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference)
for every setting.

## Verification

- `gh api repos/<owner>/<repo>/automated-security-fixes` reports `"enabled":true`.
- The repository's Insights, Dependency graph, Dependabot page lists all three ecosystems with a
  recent check and no configuration error.
- The first pull requests carry `Type: Maintenance` and run the merge checks.
