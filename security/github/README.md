# GitHub private vulnerability reporting

A security-policy starting point for a public GitHub repository whose maintainers have chosen to
receive reports through GitHub's private vulnerability-reporting form. It works independently of
the project's language and license. It does not select a support window or response-time promise.

## Files

| Payload | Destination | Mode | Placeholders |
| --- | --- | --- | --- |
| `SECURITY.md.tmpl` | `SECURITY.md` | Filled; Supported versions and Handling reports sections owned | `{{PROJECT_NAME}}`, `{{REPO_URL}}`, `{{SUPPORTED_VERSIONS}}`, `{{REPORT_HANDLING}}` |

`{{REPO_URL}}` is the public GitHub repository URL, without a trailing slash. This variant uses
that repository for both private vulnerability reports and ordinary public issues.

## Before adoption

The maintainer decides:

- Who monitors incoming reports, with repository access and notification settings that let them
  receive and handle private reports.
- Which releases or maintained branches receive security fixes. Write that decision as the
  `{{SUPPORTED_VERSIONS}}` section; do not assume that only the latest release is supported.
- How reports are handled, what response expectations can be met, and how fixes are announced.
  Write those decisions as the `{{REPORT_HANDLING}}` section. Do not invent an acknowledgement
  deadline, fix deadline, or announcement channel.

Both policy sections are owned after copying. Keep them aligned with the support the maintainer
actually provides. If these decisions are unresolved, leave adoption pending rather than
publishing the markers or treating illustrative wording as a commitment.

## Installation

1. Follow GitHub's
   [private-reporting setup](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)
   to enable private vulnerability reporting for the destination repository and configure the
   responsible maintainers' notifications. Repository owners or administrators can enable it in
   Settings, under Security and quality, Advanced Security.
2. Copy `SECURITY.md.tmpl` to `SECURITY.md` at the repository root, fill the project name and
   repository URL, and write the two owned policy sections from the decisions above.
3. Link the policy from the adopting repository's contributor guidance or README. If its
   contribution policy has a filled reporting section, add the link in an owned section or the
   owned README rather than silently changing verbatim or filled wording. Use a repository URL
   when the link also needs to work from a published package that omits `SECURITY.md`.
4. Review the rendered policy and reporting route before publishing it on the default branch.
   Record the component, source revision, filled values, and owned sections as described in
   [Maintenance](../../docs/maintenance.md).

## Verification

- No placeholder remains, and both owned sections state the maintainer's actual decisions,
  including supported versions, handling expectations, and fix announcements.
- Check the setting with the GitHub CLI, substituting the destination owner and repository:

  ```bash
  gh api repos/<owner>/<repo>/private-vulnerability-reporting
  ```

  The response must contain `"enabled": true`. An authentication or permission error does not
  establish that reporting is enabled or disabled; resolve it with an account allowed to check.
- Open the rendered private-report link while signed in and verify that it reaches the intended
  repository's report form. Do not submit a test vulnerability report. Confirm the responsible
  maintainers have configured notifications and know where to review incoming reports.
- Confirm ordinary public-issue links still work and the contributor guidance makes the private
  route discoverable. Recheck the route when moving the repository or changing the policy.

GitHub documents the setting and its API in the
[repository API reference](https://docs.github.com/en/rest/repos/repos#check-if-private-vulnerability-reporting-is-enabled-for-a-repository).
