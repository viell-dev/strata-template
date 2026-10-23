# Rust library verification recipe

Commands for a standalone Cargo library, in three stages, and a release procedure that runs them
on the commit being released. Copy the applicable commands into the adopting repository's
contributor guide or check script. The recipe supplies no toolchain file, MSRV policy, license,
package metadata, or dependency list.

## Lockfile choices

Each adopter chooses and documents its lockfile policy. A tracked `Cargo.lock` records a checkout's
resolution; an untracked one may still be reused locally. A clean checkout without one resolves
dependencies afresh. A particular verification run can also retain its own recoverable lockfile.

To retain a prepared resolution, add `--locked` to dependency-resolving Cargo commands such as
`clippy`, `test`, `doc`, and `package`, consistently in local instructions and CI. It fails if the
lockfile is absent or needs updating; prepare a usable resolution for every compiler first.
`cargo fmt` and rustup commands do not take this flag. The examples omit it to allow either policy.

Testing an existing resolution and deliberately refreshing compatible dependencies answer different
questions. The extracted package can have a different resolution, and a library's lockfile does
not constrain its consumers. See Cargo's
[lockfile guide](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html) and
[`--locked` reference](https://doc.rust-lang.org/cargo/commands/cargo-test.html#manifest-options).

## Fast checks

Run on every change with the development compiler, the one `rust-toolchain.toml` selects:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-targets --all-features
cargo test --doc --all-features
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --all-features
```

Keep the doctest line: `--all-targets` does not include documentation tests. The development
toolchain needs the `rustfmt` and `clippy` components; list them in `rust-toolchain.toml` or install
them explicitly when setting up the compiler.

### Feature configurations

`--all-features` is one configuration. It can miss code behind `cfg(not(feature = "..."))`, and
mutually exclusive features can make it invalid. Choose meaningful supported configurations:

- Default features, using the test commands without `--all-features`.
- `--no-default-features`, if supported; this does not itself mean `no_std`.
- Selected `--features <names>` combinations, and `--all-features` when valid.

Use that selection in development, MSRV, and extracted-package tests, with separate doctests, and
in relevant Clippy/documentation checks. The adopter owns the selection; no exhaustive matrix is
required.

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

## Optional hardening checks

These optional references are separate from the normal merge/release checks. Select them when the
crate needs them, and keep setup, frequency, results, and exclusions in its own documentation.

### Miri

Use [Miri](optional-checks.md#miri) when interpreting the crate's tests can help check unsafe code.
Choose a compatible dated nightly and record exclusions in the adopting repository.

### A 32-bit target

Use a [native 32-bit check](optional-checks.md#a-32-bit-target) when the crate supports that target.
The host must supply its linker, libraries, and an execution environment.

### WebAssembly

The [WebAssembly reference](webassembly.md) distinguishes library builds, JavaScript tests, and
WASI execution. Choose only the environments the adopter intends to support.

## Release procedure

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `RELEASING.md.tmpl` | `RELEASING.md` | Owned | `{{PROJECT_NAME}}` |

Fill the project name, then adapt the owned procedure to the repository's package layout,
lockfile choice, changelog (if any), and permitted merge method. Keep its verification commands
aligned with the contributor guide and workflows.

The procedure prepares a release through a PR, checks its head, then verifies the resulting merge
commit before tagging. If merging changes the SHA, rerun the gate on that final commit; a true
fast-forward preserves it, while host rebase/squash operations may not. Follow branch protection
and review requirements. The payload explains when an existing CI result can be reused.

Contributors need the fast checks and a repository-URL link to `RELEASING.md` that also works from
the published package.
