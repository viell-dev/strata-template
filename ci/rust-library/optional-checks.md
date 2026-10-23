# Optional Rust verification

Use these references when the crate's implementation or supported targets warrant extra checks.
The [core recipe](README.md) and supplied workflows do not require them. Each adopter owns the
selected toolchains, runtimes, feature combinations, commands, and execution frequency. Record
results and exclusions before claiming coverage.

## Miri

[Miri](https://github.com/rust-lang/miri#using-miri) interprets tests and can detect undefined
behavior on the paths they exercise. Choose and record a dated nightly that provides Miri and
works with the crate, then substitute it below:

```bash
miri_toolchain=nightly-YYYY-MM-DD
rustup toolchain install "$miri_toolchain" --profile minimal --component miri --component rust-src
cargo +"$miri_toolchain" miri setup
cargo +"$miri_toolchain" miri test --all-features
```

Record the tested commit, nightly, target, flags, and any skipped tests with their reasons. This
default test command does not exercise benchmark targets. Miri supports only some platform
operations, and a passing run does not prove all inputs or thread interleavings correct. A claim
of Miri coverage should link to the recorded command and result.

## A 32-bit target

For a crate that supports 32-bit Linux, the following runs its targets and doctests using the
development compiler on an x86-64 Linux host:

```bash
rustup target add i686-unknown-linux-gnu
cargo test --all-targets --all-features --target i686-unknown-linux-gnu
cargo test --doc --all-features --target i686-unknown-linux-gnu
```

Installing Rust's target standard library is only one prerequisite. The host also needs a linker
and C libraries for 32-bit GNU/Linux, and must be able to execute the resulting binaries. On
Debian or Ubuntu, the native multilib setup commonly uses `gcc-multilib` and `libc6-dev-i386`;
other hosts need their own setup or a suitable runner. Check the output for tests actually run,
including whether that Cargo version supports cross-target doctests. A compile-only check does
not exercise runtime differences such as pointer-width limits, and this target does not establish
support for other 32-bit platforms.

## WebAssembly

The [WebAssembly recipe](webassembly.md) covers library builds, portable tests in Node.js with
`wasm-bindgen-test`, and WASI tests in Wasmtime. These are separate checks with different runtime
contracts; choose the ones the crate supports. They can use `std`, and do not imply `no_std`
support. The recipe also covers testing a separate Serde deserializer adapter when one exists.
