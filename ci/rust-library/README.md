# Rust library verification recipe

Commands for a standalone Cargo library, in three stages. Copy the applicable ones into the
adopting repository's contributor guide or check script. The recipe supplies no toolchain file,
MSRV policy, license, package metadata, or dependency list.

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
constant, with a toolchain of that version installed:

```bash
# Set to this crate's actual rust-version.
msrv=1.87.0
cargo +"$msrv" test --all-targets --all-features
cargo +"$msrv" test --doc --all-features
```

Raising the minimum when a new feature requires it is allowed: update the manifest and release
notes, then verify that version. No support window, synchronized pins across crates, or scheduled
compiler upgrades are implied. Add feature combinations when features exist, and name the
supported targets before promising a platform matrix; one Linux host proves nothing about Windows
or macOS.

## Release gate

From a clean checkout of the release candidate, without `--allow-dirty`:

```bash
cargo package --list
cargo package
# Then, inside target/package/<name>-<version>/:
cargo test --all-features
```

Inspect the listing for every file the README and licensing documents link to, and for tests,
examples, or benchmarks that should ship. Testing the extracted copy confirms the published source
is testable as shipped. Record the host, compiler versions, commands, and ignored tests for the
exact release commit. The recipe ends here; it does not publish.
