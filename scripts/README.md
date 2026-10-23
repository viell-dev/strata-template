# Catalog validation

Run from the repository root with Python 3.10 or newer, Git, and Bash:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/check.py
.venv/bin/python -m unittest discover -s tests -v
```

The dependencies parse Markdown and YAML; validation itself needs no network. Setup downloads the
pinned packages. On Windows, use `.venv/Scripts/python` and make Git and Bash available on `PATH`.
The checker also accepts `--root <checkout>` so a prepared catalog can be checked explicitly.

## Checks

- Markdown links, images, and heading anchors in repository documentation, including reference
  links. Fenced examples are parsed as code, and external links are left for a separate check.
- Declared placeholders and a representative rendering of every payload, with its presence in the
  adjacent component's file table. Workflow expressions remain host expressions.
- Both installed license/contribution variants' downstream-relative Markdown links, with release
  and security-policy fixtures.
- Exact license-payload hashes, identical MIT-0 copies, label fields/colors/description lengths,
  and label documentation.
- Issue front matter and its catalog labels; YAML parsing with duplicate-key rejection; basic
  workflow structure, full-SHA action references, GitHub permissions/checkout credentials, and Bash
  syntax for every rendered shell step.
- Identical merge/release fast commands and separate all-targets/doctest package checks in the Rust
  adapters.

The tests intentionally break representative inputs and require rejection, as well as checking
successful rendering. They use disposable directories and do not edit this checkout or adopters.

## Full GitHub workflow linting

If [actionlint](https://github.com/rhysd/actionlint) is on `PATH`, the checker also runs it against
the real GitHub workflow and every rendered GitHub adapter. Alternatively pass
`--actionlint /path/to/actionlint`. Without it, the command reports that only the built-in YAML and
Bash checks ran. CI always supplies actionlint; its workflow pins version 1.7.12 and verifies the
release archive's SHA-256 before extraction. Review both values when updating the tool.

Forgejo payloads receive YAML and Bash checks, not GitHub-specific actionlint rules. These checks
do not replace Cargo execution, browser rendering, external-link checks, or actual runner tests.
They do not validate every host option, raw HTML link, licensing interpretation, or supported
feature/runtime combination. Keep those checks and their evidence in the relevant component.

## Maintaining checks

Add fixture values when adding a placeholder, and keep new payloads in their adjacent file tables.
Extend the installed fixtures when a component adds a local link dependency. For a new failure
mode, add a negative regression case alongside a valid example.

`license-hashes.json` records the payload bytes compared with the linked Mozilla/SPDX canonical
texts during initial setup. Wrapping and MIT-0 notice placeholders are repository-specific; the
license wording was compared after normalizing those differences. Do not refresh the hashes just
to make a failure pass: first compare the changed text with its canonical source and review why
it changed. License and contribution scope changes still follow
[Maintenance](../docs/maintenance.md).

Keep these checks focused on defects in this catalog and its rendered examples. They do not inspect
adopting repositories, enforce a shared layout there, or require copies to match the latest source.
The checker and its Python dependencies are maintained here and are not adopted with a component.
Updates to adopted material follow the manual or agent-assisted procedure in
[Maintenance](../docs/maintenance.md).
