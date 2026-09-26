# Contribution policies and PR prompts

Contribution terms and a pull-request prompt that points contributors at them. They depend on the
selected license, not on the programming language, so they are chosen separately from
[license material](../license/README.md) and must agree with it.

| Variant | Requires | Contains |
| --- | --- | --- |
| [mpl-2.0-rust/](mpl-2.0-rust/README.md) | [license/mpl-2.0-rust](../license/mpl-2.0-rust/README.md) | Inbound=outbound MPL-2.0 terms, the example-material dual-license grant, endorsement of the statement of intent, and a PR prompt with the recorded assent sentence |
| [mit-0/](mit-0/README.md) | [license/mit-0](../license/mit-0/README.md) | Inbound=outbound MIT-0 terms and a general PR prompt |

Every `CONTRIBUTING.md` payload has an owned Development section marked `{{DEVELOPMENT}}`. It
describes that repository's real workflow: Cargo, a JavaScript package manager, Python tooling,
site builds, deployment checks, or whatever applies. No command set or runtime version is
inserted by these components.

Security contacts, response commitments, and conduct policies are not part of any variant. Add
them only once the maintainer has chosen a policy they can administer.
