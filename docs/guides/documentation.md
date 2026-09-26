# Guide: documentation repository

A checklist for a repository that publishes Markdown only, such as an ecosystem hub, under MIT-0.
Each step links to the component's own instructions, which stay authoritative.

| Step | Component | Variant |
| --- | --- | --- |
| 1 | [license](../../license/README.md) | [mit-0](../../license/mit-0/README.md) |
| 2 | [contributing](../../contributing/README.md) | [mit-0](../../contributing/mit-0/README.md) |
| 3 | [issues](../../issues/README.md) | `proposal`, optionally a customized `bug-report` |
| 4 | [ci](../../ci/README.md) | [documentation](../../ci/documentation/README.md) |

## 1. License

Copy `LICENSE.tmpl` to `LICENSE` and fill the notice line. Add the README section payload as a
`## License` section and extend it if the repository documents projects that are licensed
differently, so readers do not take the repository's license for theirs.

## 2. Contribution policy

Copy `CONTRIBUTING.md`, fill the project name and repository URL, and write the Development
section: the tools in use, the Markdown conventions (wrap width, style), and how to check a change.
Everything but the Licensing section is owned, so a hub that routes issues to other repositories
or explains package naming should say so here. The PR prompt is optional; fill its repository URL
if used.

## 3. Issue prompts

The proposal prompt fits questions and suggestions. A bug-report prompt is for rendering or link
problems; adjust its environment question or omit it. Keep an unstructured path for questions
that fit no form.

## 4. Verification

Choose from the documentation outline: local links and assets, Markdown style, and external links
checked separately. Record the commands in the Development section.

## 5. Check the result

- No `{{` remains in any copied file, and relative links resolve.
- `LICENSE` differs from its source only on the notice line.

## 6. Record the selection

Note the components, variants, source revision, and rendered values as described in
[Maintenance](../maintenance.md).
