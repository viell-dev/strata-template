# Rust library verification recipe

Commands for a standalone Cargo library, in three stages, and a release procedure that runs them
on the commit being released. Copy the applicable commands into the adopting repository's
contributor guide or check script. The recipe supplies no toolchain file, MSRV policy, license,
package metadata, or dependency list.

## Fast checks

Run on every change with the development compiler, the one `rust-toolchain.toml` selects:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-targets --all-features
cargo test --doc --all-features
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features
```

Keep the doctest line: `--all-targets` does not include documentation tests.

## Minimum supported Rust version

Check the minimum the crate declares in `Cargo.toml` (`rust-version`), not an ecosystem-wide
constant, with a toolchain of exactly that version:

```bash
# Set to this crate's actual rust-version.
msrv=1.87.0
rustup toolchain install "$msrv" --profile minimal
cargo +"$msrv" test --all-targets --all-features
cargo +"$msrv" test --doc --all-features
```

Raising the minimum when a new feature requires it is allowed: update the manifest and release
notes, then verify that version. No support window, synchronized pins across crates, or scheduled
compiler upgrades are implied. Add feature combinations when features exist, and name the
supported targets before promising a platform matrix; one Linux host proves nothing about Windows
or macOS.

## Package

From a clean checkout, with `git status --porcelain` printing nothing and without `--allow-dirty`:

```bash
cargo package --list
cargo package
(
  cd target/package/<name>-<version> &&
  cargo test --all-targets --all-features &&
  cargo test --doc --all-features
)
```

Inspect the listing for every file the README and licensing documents link to, and for tests,
examples, or benchmarks that should ship. Testing the extracted copy confirms the published source
is testable as shipped, including its benchmark targets. Keep the separate doctest command here
too: `--all-targets` does not include documentation tests.

## Merge and release checks

The fast checks are the merge checks: every change passes them before it is merged. The three
stages together are the release checks, run on the commit to be tagged. CI can run either set;
the [github](../github/README.md) and [forgejo](../forgejo/README.md) adapters each supply
a `rust-library-` workflow payload for both.

## Release procedure

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `RELEASING.md.tmpl` | `RELEASING.md` | Filled | `{{PROJECT_NAME}}` |

The three stages together, run on the exact commit to be tagged, are the release gate. The
payload is the maintainers' procedure around it: prepare the release commit in a pull request,
run the gate on its head commit, report the host, compiler versions, results, and ignored tests
in the pull request, merge with a fast-forward, then tag and publish. A passing CI run of the
first two stages on that commit may be cited instead of repeating them.
Contributors need only the fast checks, so put those in the contributor guide and link to
`RELEASING.md` using its repository URL so the link also works from the published package.
