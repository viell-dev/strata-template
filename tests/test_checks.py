"""Positive and negative fixtures for the catalog validator; no network or Cargo required."""

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("catalog", ROOT / "scripts/check.py")
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="strata-template-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for path in catalog.files(ROOT):
            destination = self.root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, destination)
        subprocess.run(
            ["git", "init", "-q", "--initial-branch=main"], cwd=self.root, check=True,
        )

    def replace(self, path, before, after):
        file = self.root / path
        text = file.read_text()
        self.assertIn(before, text)
        file.write_text(text.replace(before, after))

    def reject(self, message):
        with self.assertRaisesRegex(catalog.CatalogError, message):
            catalog.check(self.root)

    def test_catalog_passes(self):
        _, payloads = catalog.check(self.root)
        self.assertEqual(payloads, len(list(self.root.rglob("*.tmpl"))))

    def test_reference_link_to_missing_file_fails(self):
        with (self.root / "README.md").open("a") as file:
            file.write("\n[Missing][target]\n\n[target]: no-such-file.md\n")
        self.reject("missing local target")

    def test_missing_heading_fails(self):
        with (self.root / "README.md").open("a") as file:
            file.write("\n[Missing](README.md#no-such-heading)\n")
        self.reject("missing heading")

    def test_fenced_example_link_is_ignored(self):
        with (self.root / "README.md").open("a") as file:
            file.write("\n```markdown\n[Example](not-a-real-target)\n```\n")
        catalog.check(self.root)

    def test_undeclared_placeholder_fails(self):
        self.replace("security/github/SECURITY.md.tmpl", "{{PROJECT_NAME}}", "{{UNDECLARED}}")
        self.reject("undeclared placeholders")

    def test_license_mutation_fails(self):
        with (self.root / "license/mpl-2.0-rust/LICENSE.tmpl").open("a") as file:
            file.write("Changed terms\n")
        self.reject("license text changed")

    def test_bad_label_color_fails(self):
        self.replace("labels/labels.json.tmpl", '"d73a4a"', '"NOTHEX"')
        self.reject("invalid label color")

    def test_duplicate_label_fails(self):
        path = self.root / "labels/labels.json.tmpl"
        labels = json.loads(path.read_text())
        labels.append(labels[0])
        path.write_text(json.dumps(labels))
        self.reject("duplicate/empty label")

    def test_downstream_relative_link_is_checked_after_rendering(self):
        self.replace("license/mit-0/README-LICENSE.md.tmpl", "](LICENSE)", "](MISSING-LICENSE)")
        self.reject("missing local target")

    def test_comment_inside_action_value_fails(self):
        self.replace(
            "ci/github/rust-library-merge-checks.yml.tmpl",
            '{{CHECKOUT_ACTION}}"', '{{CHECKOUT_ACTION}} # v6.1.0"',
        )
        self.reject("action reference must end")

    def test_duplicate_yaml_key_fails(self):
        with (self.root / "ci/github/rust-library-merge-checks.yml.tmpl").open("a") as file:
            file.write("jobs: {}\n")
        self.reject("duplicate YAML key")

    def test_invalid_shell_fails(self):
        self.replace("ci/github/rust-library-merge-checks.yml.tmpl", "cargo fmt --check", "echo '")
        self.reject("invalid shell syntax")

    def test_persisted_github_credentials_fail(self):
        self.replace(
            "ci/github/rust-library-merge-checks.yml.tmpl",
            "persist-credentials: false", "persist-credentials: true",
        )
        self.reject("checkout must discard credentials")

    def test_missing_package_doctests_fail(self):
        path = self.root / "ci/github/rust-library-release-checks.yml.tmpl"
        text = path.read_text()
        before, _, after = text.rpartition("cargo test --doc --all-features")
        path.write_text(before + "true" + after)
        self.reject("missing extracted-package check")

    def test_fast_command_drift_fails(self):
        self.replace("ci/github/rust-library-merge-checks.yml.tmpl", "cargo fmt --check", "cargo fmt")
        self.reject("merge/release fast commands diverge")

    def test_public_mdrefine_manifest_fails(self):
        self.replace("ci/mdrefine/package.json.tmpl", '"private": true', '"private": false')
        self.reject("manifest must be private")

    def test_mdrefine_version_in_payload_fails(self):
        self.replace(
            "ci/mdrefine/package.json.tmpl",
            '"private": true\n', '"private": true,\n  "devDependencies": { "mdrefine": "0.4.0" }\n',
        )
        self.reject("must not declare dependencies")

    def test_commented_mdrefine_config_fails(self):
        self.replace("ci/mdrefine/mdtools.config.jsonc.tmpl", "{\n", "{\n  // Comment\n")
        self.reject("invalid JSON")

    def test_mdrefine_host_command_drift_fails(self):
        self.replace(
            "ci/forgejo/mdrefine-merge-checks.yml.tmpl",
            "mdrefine lint --max-warnings 0", "mdrefine lint",
        )
        self.reject("host workflow commands diverge")

    def test_mdrefine_run_by_command_name_fails(self):
        self.replace(
            "ci/github/mdrefine-merge-checks.yml.tmpl",
            "npx --no-install mdrefine lint", "npx --no-install mdtools lint",
        )
        self.reject("`npx mdtools` can fetch an unrelated package")

    def test_mdrefine_command_missing_from_recipe_fails(self):
        for host in ("github", "forgejo"):
            self.replace(
                f"ci/{host}/mdrefine-merge-checks.yml.tmpl",
                "npm ci --ignore-scripts", "npm ci",
            )
        self.reject("workflow command missing from recipe")

    def test_unknown_prompt_label_fails(self):
        self.replace("issues/bug-report.md.tmpl", '"Type: Bug"', '"Undefined Label"')
        self.reject("unknown issue labels")


if __name__ == "__main__":
    unittest.main()
