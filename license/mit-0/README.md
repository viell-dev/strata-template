# MIT-0

MIT No Attribution for a whole project: copy, adapt, and reuse freely, no attribution required.
There is no compilation clarification or example-material carveout, because the license already
permits everything those would add.

## Files

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `LICENSE.tmpl` | `LICENSE` | Filled | `{{YEAR}}`, `{{COPYRIGHT_HOLDER}}` |
| `README-LICENSE.md.tmpl` | The `## License` section of `README.md` | Owned section | None |

Only the notice line may change; the text must keep matching the `MIT-0` SPDX identifier.

## Installation

1. Copy `LICENSE.tmpl` to `LICENSE` and fill the notice line.
2. Add a License section to the README. The payload is a starting sentence; extend it when the
   repository's scope needs explaining, for example when the repository documents projects that
   are licensed differently.
3. Optionally install [contributing/mit-0](../../contributing/mit-0/README.md).

Where the stack has package metadata (Cargo, npm, Python packaging), set its license field to
`MIT-0`.

## Verification

- No placeholder remains in `LICENSE`; its only difference from the payload is the notice line.
- The README's License section links to the copied `LICENSE` and describes the repository's scope.
- Any package metadata uses the same `MIT-0` identifier.
