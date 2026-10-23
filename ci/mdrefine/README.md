# mdrefine Markdown recipe

Lints and formats a repository's Markdown with [mdrefine](https://www.npmjs.com/package/mdrefine).
It reports style findings and rewrites them, reads tables, alerts, and other syntax as the hosting
forge renders them, and checks local links and their heading fragments. The recipe suits the
documents of any repository, whatever its main language, and covers the
[documentation outline](../documentation/README.md)'s style and local-link checks. External links
are not checked; keep that check separate.

mdrefine is maintained in
[viell-dev/slop-markdown-tools](https://github.com/viell-dev/slop-markdown-tools), and its
[documentation](https://viell-dev.github.io/slop-markdown-tools/) is authoritative for rules,
options, and command behavior. Selecting the recipe brings an npm manifest and lockfile into the
repository; contributors and runners need Node.js 22.12 or newer.

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `package.json.tmpl` | `package.json` | Owned | `{{PROJECT_NAME}}` |
| `mdtools.config.jsonc.tmpl` | `mdtools.config.jsonc` | Owned | None |

## Configuration

The configuration extends mdrefine's `recommended` and `github` presets and changes two of their
defaults to match existing Strata documents: prose wraps at 100 columns instead of 80, and tables
keep compact `| --- |` delimiter rows instead of being padded into aligned columns. Everything else
follows the presets, including `_emphasis_`, `**strong**` text, `-` bullets, `#` headings, backtick
fences, and warnings about problems that show on the rendered page.

For documents rendered by another forge, replace `github` with `forgejo` (also for Codeberg) or
`gitea`, as listed in mdrefine's
[presets](https://viell-dev.github.io/slop-markdown-tools/configuration.html#presets). Add `ignore`
patterns for generated or deliberately unformatted Markdown. Files that Git ignores, nested
repositories, and `node_modules/` are skipped already.

## Setup

1. Copy both payloads to the repository root. Fill `{{PROJECT_NAME}}` with a valid npm package
   name, normally the repository name: without a name, `npm install` records the checkout's
   directory name in the lockfile, which differs between clones and worktrees. `private` keeps the
   manifest from being published. If the repository already has a `package.json`, use that
   instead.
2. Add `node_modules/` to `.gitignore`, and install the current release:

   ```bash
   npm install --save-dev --save-exact mdrefine@latest
   ```

   This records its exact version in `package.json` and `package-lock.json`. If that release is
   newer than the one this recipe was last checked with, adapt the configuration to it before
   reformatting; see [Versions and updates](#versions-and-updates). Track `package.json`,
   `package-lock.json`, and `mdtools.config.jsonc`.
3. Reformat the existing documents in a commit of their own. Preview the changes with
   `npx --no-install mdrefine format --diff`, apply them with
   `npx --no-install mdrefine format --write`, and review the result. Filling paragraphs to the
   wrap width usually changes most hand-wrapped prose the first time. Then fix by hand what the
   lint check still reports, such as broken links.
4. Put the checks below into the contributor guide's Development section or the repository's
   check script, with `npx --no-install mdrefine format --write` as the fix for style findings.
5. In a Rust crate, keep the three files out of the published package. An explicit `include` list
   already leaves them out; otherwise add them to `exclude`.
6. To run the checks on pull requests, copy the host adapter's `mdrefine-merge-checks.yml.tmpl`:
   [github](../github/README.md#markdown-checks) or [forgejo](../forgejo/README.md#markdown-checks).

## Checks

From the repository root:

```bash
npm ci --ignore-scripts
npx --no-install mdrefine lint --max-warnings 0
npx --no-install mdrefine format --check
```

`npm ci` installs exactly the locked versions and fails when the lockfile and manifest disagree.
`--ignore-scripts` keeps dependency install scripts from running; mdrefine needs none.
`npx --no-install mdrefine` runs the installed mdrefine's command and never downloads anything.
Invoke it through the package name: the command itself is named `mdtools`, but an unrelated npm
package has that name, and where mdrefine is not installed, `npx mdtools` fetches that one instead.

`lint` reports problems such as broken links as errors and style findings as warnings;
`--max-warnings 0` makes both fail. `format --check` writes nothing and fails when any document
would change. Both commands exit with `1` for findings and `2` when they cannot run.

## Versions and updates

The recipe names no mdrefine version: setup installs the current release, and the repository pins
it exactly, so every checkout and runner formats the same way. Before 1.0, a minor release may
change what formatting produces or what the configuration accepts, and even a patch release may
format a document differently where an earlier release mishandled it; see mdrefine's
[versioning policy](https://viell-dev.github.io/slop-markdown-tools/versions.html). The exact pin
makes each such change an explicit update.

This recipe was last checked with mdrefine 0.4.0. With a later release, read the changelogs since
then and check the configuration against the current
[documentation](https://viell-dev.github.io/slop-markdown-tools/): presets, rule names, and the
options it sets may have changed. Both checks exit with `2` when the configuration names an unknown
preset, rule, or option, or gives an option a value the release does not accept.

To move to a new release, read its changelog, then run:

```bash
npm install --save-dev --save-exact mdrefine@latest
npx --no-install mdrefine format --write
```

Commit the version change together with the reformatting it causes, so that the checks pass on
that commit.

On GitHub, Dependabot can propose these updates. Add an `npm` entry to the repository's
`.github/dependabot.yml`, beside its other ecosystems:

```yaml
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "monthly"
    cooldown:
      default-days: 7
    labels:
      - "Type: Maintenance"
```

When an update formats documents differently, its Markdown checks fail. Run `format --write` on
Dependabot's branch and push the result, or make the update by hand. Dependabot stops rebasing a
pull request once someone else has pushed to it.

## Verification

- `npm ci --ignore-scripts` succeeds in a clean checkout, and `npx --no-install mdrefine --version`
  prints the version recorded in `package.json`.
- Both checks pass on the reformatted repository and fail after a deliberate defect, such as
  emphasis written as `*text*` or a link to a missing file.
- `node_modules/` is ignored, and the manifest, lockfile, and configuration are tracked.
- In a Rust crate, `cargo package --list` shows none of the three files.

The rendered payloads, setup install, and commands have been checked locally with mdrefine 0.4.0
under Node.js 24 and 22: an exact version recorded by setup, a clean install without install
scripts, passing checks on formatted documents, failing checks for a style defect and a missing link
target, and an unchanged lockfile after `npm install` in a checkout with a different directory name.
An unknown preset, rule, or option made both checks exit with `2`.
