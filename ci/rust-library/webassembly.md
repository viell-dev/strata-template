# Optional WebAssembly verification

Use this alongside the [Rust library recipe](README.md#optional-hardening-checks) when an adopter
wants WebAssembly coverage. Choose the target, runtime, feature combinations, and execution
frequency in that repository. These checks are optional and are not in the workflow adapters.

WebAssembly does not require `no_std`. Both targets below provide `std`, but their available host
services differ. In-memory operations can work where filesystem access or thread creation cannot.
Consult Rust's target documentation before deciding which APIs and tests to support:

- [`wasm32-unknown-unknown`](https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html)
  makes few host assumptions; JavaScript embeddings normally provide their own bindings.
- [`wasm32-wasip1`](https://doc.rust-lang.org/rustc/platform-support/wasm32-wasip1.html) uses WASI
  Preview 1 host interfaces. Running it in Wasmtime does not establish browser compatibility.

Keep the [native 32-bit check](README.md#a-32-bit-target) when that platform is supported. Wasm's
32-bit pointers do not reproduce native operating-system or concurrency behavior.

### A future wasm64 check

[`wasm64-unknown-unknown`](https://doc.rust-lang.org/rustc/platform-support/wasm64-unknown-unknown.html)
uses 64-bit pointers and memory addresses. It is relevant to larger in-memory workloads and can
expose assumptions that all Wasm pointers fit in 32 bits. Memory64 is part of
[Wasm 3.0](https://webassembly.org/news/2025-09-17-wasm-3.0/), and
[wasm-bindgen 0.2.120](https://github.com/wasm-bindgen/wasm-bindgen/releases/tag/0.2.120) added support.

As checked on 2026-10-22, Rust still classifies this target as Tier 3 and ships no prebuilt standard
library for it. An experiment needs a compatible runtime and a custom-built `std`, commonly using
a dated nightly with `rust-src` and Cargo's `-Z build-std`. Treat that as a separate experimental
check; the commands and test attributes below cover wasm32 only. No wasm64 execution is claimed
by this recipe. Serde interoperability does not itself require either pointer width.

## Build the library

With the adopter's selected compiler:

```bash
rustup target add wasm32-unknown-unknown wasm32-wasip1
cargo build --lib --target wasm32-unknown-unknown
cargo build --lib --target wasm32-wasip1
```

These commands use default features. Repeat with each feature combination the adopter supports
on that target, including `--all-features` when applicable. Apply the recipe's
[lockfile choice](README.md#lockfile-choices) consistently. A library build checks compilation of
the library and its normal dependencies; it does not execute code or validate a final embedding.

## Run portable tests in Node.js

Use [`wasm-bindgen-test`](https://wasm-bindgen.github.io/wasm-bindgen/wasm-bindgen-test/usage.html)
for a JavaScript runtime. Add its development dependency for this target in `Cargo.toml`, choosing
a version compatible with the compiler used for these tests:

```toml
[target.'cfg(all(target_arch = "wasm32", target_os = "unknown"))'.dev-dependencies]
wasm-bindgen-test = "0.3"
```

Create `tests/portable.rs`. Conditional attributes let the same assertions run in the Wasm
harness and the normal Rust test harness on native or WASI targets:

```rust
#[cfg_attr(
    all(target_arch = "wasm32", target_os = "unknown"),
    wasm_bindgen_test::wasm_bindgen_test
)]
#[cfg_attr(not(all(target_arch = "wasm32", target_os = "unknown")), test)]
fn parses_a_number() {
    assert_eq!("42".parse::<u32>().unwrap(), 42);
}
```

This sample only checks the harness. Replace its body and add cases that exercise the adopting
crate's public API, including invalid input and relevant boundary conditions. Ordinary `#[test]`
functions are not discovered by the Wasm harness; check the reported test names and counts.

Install Node.js and the `wasm-bindgen-test-runner` executable from `wasm-bindgen-cli`, following
the linked harness guide or using the project's
[release binaries](https://github.com/wasm-bindgen/wasm-bindgen/releases). The CLI must match the
resolved **`wasm-bindgen`** version, not the `wasm-bindgen-test` version. Find that resolution with:

```bash
cargo tree --target wasm32-unknown-unknown -i wasm-bindgen
```

Put the runner and Node on `PATH`, then run the selected integration target:

```bash
CARGO_TARGET_WASM32_UNKNOWN_UNKNOWN_RUNNER=wasm-bindgen-test-runner \
  cargo test --target wasm32-unknown-unknown --test portable
```

The harness uses Node by default. This proves execution in that Node version, not in browsers.
If browser execution is supported, add the harness's
[browser configuration](https://wasm-bindgen.github.io/wasm-bindgen/wasm-bindgen-test/browsers.html)
and exercise the chosen browsers separately. Do not add that configuration to a suite intended
to keep using the default Node runner.

## Run portable tests in a WASI runtime

Install a recorded version of [Wasmtime](https://docs.wasmtime.dev/cli-install.html) and put it
on `PATH`. The same integration file uses ordinary `#[test]` functions on `wasm32-wasip1`:

```bash
CARGO_TARGET_WASM32_WASIP1_RUNNER="wasmtime run" \
  cargo test --target wasm32-wasip1 --test portable -- --test-threads=1
```

This uses the normal Rust harness with one test thread. The in-memory tests need no host
directory access. Tests using files need explicit fixtures and Wasmtime directory permissions;
see its [CLI options](https://docs.wasmtime.dev/cli-options.html). WASI results apply to this
target and runtime, not every WASI version or embedding.

An assertion failure can terminate the WASI process with a trap instead of printing the usual
failed-test summary. Require a successful process exit and the expected passed-test count.

## Coverage and interoperability

Keep host-dependent tests, concurrency tests, panic-unwinding checks, and benchmark tools in
their appropriate native checks. Select a meaningful portable suite instead of assuming that
`--all-targets` or native doctests will work unchanged under a Wasm runner. Record exclusions and
why they do not apply; do not hide a required behavior behind a target condition just to pass.

For a separate Serde deserializer adapter, exercise its actual deserialization path in the same
supported target/runtime combinations when that adapter exists. Parser tests alone do not
establish adapter compatibility. This does not require adding Serde to every parser or supporting
Serde's optional [`no_std` mode](https://serde.rs/no-std.html); adapter dependencies and feature
choices belong to the adapter crate.

Record the commit, compiler, target, features, dependency resolution, runner and runtime versions,
test names/counts, and exclusions with each result. Distinguish library compilation, Node or
browser execution, and WASI execution. A passing small fixture validates the recipe setup, not
the portability of an adopting library.
