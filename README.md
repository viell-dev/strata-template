# strata-template

Reusable starting points for Strata repositories: license material, contribution policies, issue
prompts, a label catalog, dependency update configuration, security-reporting instructions, and
verification recipes. A repository selects the parts it needs, copies them, fills in the
documented placeholders, and owns the result.

Strata's core is a Rust parser stack, but the surrounding ecosystem may include editor extensions,
TypeScript or Python projects, websites, services, and infrastructure tooling. Components are
therefore grouped by concern and offered in named variants, so that license, language, repository
purpose, and hosting can be chosen independently. Selecting Rust does not select MPL-2.0, and
selecting MIT-0 does not select a build tool.

## Layout

| Directory | Purpose | Components or variants |
| --- | --- | --- |
| [license/](license/README.md) | License texts and licensing statements | `mpl-2.0-rust`, `mit-0` |
| [contributing/](contributing/README.md) | Contribution policies and PR prompts | `mpl-2.0-rust`, `mit-0` |
| [issues/](issues/README.md) | Issue prompts selected file by file | General and Rust bug reports, proposals, questions |
| [labels/](labels/README.md) | Shared issue and pull request labels | Label catalog |
| [dependencies/](dependencies/README.md) | Dependency update configuration | `dependabot-rust-library` |
| [security/](security/README.md) | Private vulnerability-reporting policy | `github` |
| [ci/](ci/README.md) | Verification recipes and runner adapters | `rust-library`, `documentation`, `github`, `forgejo` |
| [docs/guides/](docs/guides/) | End-to-end adoption checklists | [Rust library](docs/guides/rust-library.md), [documentation repository](docs/guides/documentation.md) |
| [docs/maintenance.md](docs/maintenance.md) | Selection records and updates | Ownership, source revisions, intended tooling |

Each concern has a `README.md` describing its available components. Concerns with named variants
keep each variant's instructions beside its payloads; `issues/`, `labels/`, and `dependencies/`
list their payloads directly in the concern README.

## Conventions

- **Payloads end in `.tmpl`.** A payload is a file meant to be copied into another repository.
  The suffix keeps payloads distinct from this repository's own documents: `LICENSE.tmpl` is not
  this repository's license, and a payload's downstream-relative links are not broken links here.
  Drop the suffix when copying.
- **Placeholders look like `{{NAME}}`.** The vocabulary is listed below. A rendered file must
  contain none of them. Workflow expressions such as `${{ github.ref }}` are Actions expressions, not
  placeholders.
- **Every payload has an ownership mode**, stated in its variant's file table:
  - _Verbatim_: copied byte-for-byte and never edited downstream. An update replaces the file.
  - _Filled_: placeholders replaced, otherwise identical to the source. An update is re-rendered.
  - _Owned_: a starting point that the adopting repository maintains. Upstream changes are read
    for ideas, not applied.

  A file can mix modes by section; the table says which sections are owned.

### Placeholders

| Placeholder | Meaning | Strata convention |
| --- | --- | --- |
| `{{PROJECT_NAME}}` | Package or repository name as users know it | For example `strata-reader` |
| `{{REPO_URL}}` | Upstream repository URL, without a trailing slash | `https://github.com/viell-dev/<name>` |
| `{{YEAR}}` | Year of first publication, for license notices | The real year; never backdated |
| `{{COPYRIGHT_HOLDER}}` | Name on license notices | `viell` |
| `{{DEVELOPMENT}}` | Marks an owned Development section to be written | That repository's actual workflow |
| `{{SUPPORTED_VERSIONS}}` | Marks an owned security-support section to be written | The adopter's chosen releases or maintained branches |
| `{{REPORT_HANDLING}}` | Marks an owned report-handling section to be written | The adopter's response expectations and fix announcements |
| `{{RUNNER_LABEL}}`, `{{CHECKOUT_ACTION}}`, `{{CHECK_COMMAND}}` | CI adapter inputs | See [ci/github](ci/github/README.md) and [ci/forgejo](ci/forgejo/README.md) |

## Adopting components

1. Start from a guide if one fits: [Rust library](docs/guides/rust-library.md) or
   [documentation repository](docs/guides/documentation.md). Otherwise read the concern READMEs
   and choose variants directly.
2. Copy the selected payloads to the destinations in each file table, dropping `.tmpl`.
3. Replace the placeholders and write the owned sections.
4. Check the result in the destination repository: no placeholder left, relative links resolve,
   license texts unchanged, plus whatever stack-specific checks the guide lists.
5. Record what was adopted and from which revision, as described in
   [Maintenance](docs/maintenance.md).

Omit components that do not help. Two repositories with the same license may still use different
build tools, contribution workflows, and issue prompts. Copying a directory here changes no
existing repository, and a newer template revision is an available update, not evidence that an
adopter is out of date.

## Not included

A code of conduct, changelog conventions, and toolchain pins are deliberately absent. Each needs
maintainer decisions first, such as an enforcement route or support window, before a template
would help. Add them as components once those decisions exist.

The optional [security-reporting component](security/README.md) provides a private reporting
route, but adoption still requires a monitored destination and maintainer-chosen support and
handling policies. It supplies no default commitments.

## Contributing and reuse

See [CONTRIBUTING.md](CONTRIBUTING.md). Original documentation and template authoring in this
repository are available under [MIT-0](LICENSE). Included license texts retain their own notices
and are not relicensed by this repository. Licensing statements inside payloads describe the
adopting project once applied, not this repository.
