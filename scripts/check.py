#!/usr/bin/env python3
"""Check this catalog without accessing the network or modifying an adopting repository."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
import yaml

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = MarkdownIt("commonmark").enable("table")
PLACEHOLDER = re.compile(r"(?<!\$)\{\{([A-Z][A-Z0-9_]*)\}\}")
VALUES = {
    "PROJECT_NAME": "example-library",
    "REPO_URL": "https://github.com/example/example-library",
    "YEAR": "2026",
    "COPYRIGHT_HOLDER": "Example Maintainer",
    "DEVELOPMENT": "Run the repository's documented checks.",
    "SUPPORTED_VERSIONS": "The selected maintained branch receives fixes.",
    "REPORT_HANDLING": "The maintainer coordinates assessment and disclosure with the reporter.",
    "MSRV": "1.87.0",
    "RUNNER_LABEL": "ubuntu-latest",
    "CHECKOUT_ACTION": "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803",
    "CHECK_COMMAND": 'printf "first check\\n"\n          printf "second check\\n"',
}


class CatalogError(Exception):
    """A catalog invariant failed."""


class Loader(yaml.SafeLoader):
    """Use Actions-compatible boolean keys and reject duplicate YAML mapping keys."""


Loader.yaml_implicit_resolvers = copy.deepcopy(yaml.SafeLoader.yaml_implicit_resolvers)
for key, resolvers in Loader.yaml_implicit_resolvers.items():
    Loader.yaml_implicit_resolvers[key] = [
        (tag, regex) for tag, regex in resolvers if tag != "tag:yaml.org,2002:bool"
    ]
Loader.add_implicit_resolver(
    "tag:yaml.org,2002:bool", re.compile(r"^(?:true|false|True|False|TRUE|FALSE)$"), list("tTfF")
)


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise CatalogError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def require(condition, message):
    if not condition:
        raise CatalogError(message)


def parse_yaml(text, path):
    try:
        return yaml.load(text, Loader=Loader)
    except yaml.YAMLError as error:
        raise CatalogError(f"{path}: invalid YAML: {error}") from error


def files(root):
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root, check=True, capture_output=True,
    )
    return sorted({Path(name.decode()) for name in result.stdout.split(b"\0") if name})


def inline_text(token):
    return "".join(
        child.content for child in token.children or [] if child.type in {"text", "code_inline"}
    )


def anchors(text):
    seen = set()
    result = set()
    tokens = MARKDOWN.parse(text)
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        heading = inline_text(tokens[index + 1]).lower()
        slug = "".join(
            char for char in heading
            if char in "-_ " or not unicodedata.category(char).startswith(("P", "S", "C"))
        ).replace(" ", "-")
        candidate = slug
        suffix = 0
        while candidate in seen:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        seen.add(candidate)
        result.add(candidate)
    return result


def links(text):
    for token in MARKDOWN.parse(text):
        for child in token.children or []:
            if child.type == "link_open":
                yield child.attrGet("href")
            elif child.type == "image":
                yield child.attrGet("src")


def check_links(root, path):
    for href in links((root / path).read_text()):
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        destination = ((root / path).parent / unquote(url.path)).resolve() if url.path else root / path
        require(destination.is_relative_to(root), f"{path}: link escapes repository: {href}")
        require(destination.exists(), f"{path}: missing local target: {href}")
        if url.fragment and destination.suffix == ".md" and destination.is_file():
            require(
                unquote(url.fragment) in anchors(destination.read_text()),
                f"{path}: missing heading: {href}",
            )


def render(text, path, vocabulary):
    names = set(PLACEHOLDER.findall(text))
    require(names <= vocabulary, f"{path}: undeclared placeholders: {sorted(names - vocabulary)}")
    require(names <= VALUES.keys(), f"{path}: add representative values for {sorted(names - VALUES.keys())}")
    result = PLACEHOLDER.sub(lambda match: VALUES[match[1]], text)
    require(not PLACEHOLDER.search(result), f"{path}: unrendered placeholder")
    return result


def check_labels(root):
    labels = json.loads((root / "labels/labels.json.tmpl").read_text())
    require(isinstance(labels, list) and labels, "label catalog must be a nonempty array")
    names = set()
    readme = (root / "labels/README.md").read_text()
    for label in labels:
        require(set(label) == {"name", "color", "description"}, f"invalid label fields: {label}")
        name = label["name"]
        require(isinstance(name, str) and name and name not in names, f"duplicate/empty label: {name}")
        require(re.fullmatch(r"[0-9a-f]{6}", label["color"]), f"invalid label color: {name}")
        require(0 < len(label["description"]) <= 100, f"invalid label description length: {name}")
        require(f"`{name}`" in readme, f"undocumented label: {name}")
        names.add(name)
    return names


def check_issue(text, path, labels):
    require(text.startswith("---\n"), f"{path}: missing issue front matter")
    parts = text.split("---", 2)
    require(len(parts) == 3, f"{path}: unterminated issue front matter")
    meta = parse_yaml(parts[1], path)
    require(isinstance(meta, dict), f"{path}: issue front matter must be a mapping")
    for key in ("name", "about"):
        require(isinstance(meta.get(key), str) and meta[key].strip(), f"{path}: missing {key}")
    assigned = meta.get("labels", [])
    require(isinstance(assigned, list), f"{path}: labels must be a list")
    require(set(assigned) <= labels, f"{path}: unknown issue labels")
    require(bool(parts[2].strip()), f"{path}: empty issue prompt")


def check_workflow(text, path, actionlint=None):
    data = parse_yaml(text, path)
    require(isinstance(data, dict) and "on" in data and data.get("jobs"), f"{path}: invalid workflow shape")
    require(isinstance(data["on"], dict), f"{path}: workflow events must be a mapping")
    if "github" in path.parts or ".github" in path.parts:
        require(data.get("permissions") == {"contents": "read"}, f"{path}: expected read-only permissions")
        if actionlint:
            result = subprocess.run([str(actionlint), "-"], input=text, text=True, capture_output=True)
            require(result.returncode == 0, f"{path}: actionlint: {result.stdout}{result.stderr}")
    for name, job in data["jobs"].items():
        require(job.get("timeout-minutes", 0) > 0, f"{path}: {name} needs a timeout")
        for step in job.get("steps", []):
            if "uses" in step:
                require(
                    re.search(r"@[0-9a-f]{40}$", step["uses"]),
                    f"{path}: action reference must end at a full commit SHA (comments stay outside quotes)",
                )
                if "checkout@" in step["uses"] and ("github" in path.parts or ".github" in path.parts):
                    require(
                        step.get("with", {}).get("persist-credentials") is False,
                        f"{path}: checkout must discard credentials",
                    )
            if "run" in step:
                require(isinstance(step["run"], str), f"{path}: run must be a string")
                result = subprocess.run(
                    ["bash", "-n"], input=step["run"], text=True, capture_output=True,
                )
                require(result.returncode == 0, f"{path}: invalid shell syntax: {result.stderr.strip()}")


def check_licenses(root):
    records = json.loads((root / "scripts/license-hashes.json").read_text())
    for path, record in records.items():
        actual = hashlib.sha256((root / path).read_bytes()).hexdigest()
        require(actual == record["sha256"], f"{path}: license text changed; compare with {record['source']}")
    require(
        (root / "license/mit-0/LICENSE.tmpl").read_bytes()
        == (root / "license/mpl-2.0-rust/LICENSE-MIT-0.tmpl").read_bytes(),
        "MIT-0 payload copies differ",
    )


def check_fixture_links(rendered):
    """Install both license/contribution pairs to validate downstream-relative Markdown links."""
    for variant in ("mit-0", "mpl-2.0-rust"):
        with tempfile.TemporaryDirectory(prefix="strata-template-") as directory:
            fixture = Path(directory).resolve()
            for source, text in rendered.items():
                if source.parts[:2] not in [("license", variant), ("contributing", variant)]:
                    continue
                name = source.name.removesuffix(".tmpl")
                if name == "README-LICENSE.md":
                    name = "README.md"
                elif name == "pull_request_template.md":
                    name = ".github/pull_request_template.md"
                destination = fixture / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(text)
            for name, source in [
                ("RELEASING.md", "ci/rust-library/RELEASING.md.tmpl"),
                ("SECURITY.md", "security/github/SECURITY.md.tmpl"),
            ]:
                (fixture / name).write_text(rendered[Path(source)])
            for path in fixture.rglob("*.md"):
                check_links(fixture, path.relative_to(fixture))


def check(root, actionlint=None):
    root = root.resolve()
    paths = files(root)
    vocabulary = set()
    for line in (root / "README.md").read_text().splitlines():
        if line.startswith("| `{{"):
            vocabulary.update(PLACEHOLDER.findall(line))
    labels = check_labels(root)
    check_licenses(root)
    rendered = {}
    for path in paths:
        if path.suffix == ".md":
            check_links(root, path)
        if path.suffix == ".tmpl":
            text = render((root / path).read_text(), path, vocabulary)
            rendered[path] = text
            readme = root / path.parent / "README.md"
            require(readme.exists() and f"`{path.name}`" in readme.read_text(), f"{path}: missing file-table entry")
            if path.name.endswith(".yml.tmpl"):
                if path.parts[0] == "ci":
                    check_workflow(text, path, actionlint)
                else:
                    require(parse_yaml(text, path).get("version") == 2, f"{path}: invalid Dependabot version")
            elif path.parts[0] == "issues":
                check_issue(text, path, labels)
        elif path.parts[:2] == (".github", "workflows") and path.suffix in {".yml", ".yaml"}:
            check_workflow((root / path).read_text(), path, actionlint)
        elif path.parts[:2] == (".github", "ISSUE_TEMPLATE") and path.suffix == ".md":
            check_issue((root / path).read_text(), path, labels)
    check_fixture_links(rendered)
    # The separate doctest command is part of the recipe in both hosts, for every fast stage.
    for host in ("github", "forgejo"):
        merge = parse_yaml(rendered[Path(f"ci/{host}/rust-library-merge-checks.yml.tmpl")], host)
        release = parse_yaml(rendered[Path(f"ci/{host}/rust-library-release-checks.yml.tmpl")], host)
        runs = lambda job: [step["run"] for step in job["steps"] if "run" in step]
        fast = runs(merge["jobs"]["fast"])
        require(fast == runs(release["jobs"]["fast"]), f"{host}: merge/release fast commands diverge")
        for command in ("cargo test --all-targets --all-features", "cargo test --doc --all-features"):
            require(command in fast, f"{host}: missing fast check: {command}")
            package = "\n".join(runs(release["jobs"]["package"]))
            require(command in package, f"{host}: missing extracted-package check: {command}")
    return len(paths), len(rendered)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="catalog checkout to validate")
    parser.add_argument(
        "--actionlint", type=Path, default=shutil.which("actionlint"),
        help="actionlint executable; detected on PATH when available",
    )
    args = parser.parse_args()
    try:
        count, payloads = check(args.root, args.actionlint)
    except (CatalogError, OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"Catalog check failed: {error}", file=sys.stderr)
        return 1
    print(f"Catalog checks passed: {count} files, {payloads} rendered payloads")
    if not args.actionlint:
        print("actionlint not installed: only YAML structure and Bash syntax checked for workflows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
