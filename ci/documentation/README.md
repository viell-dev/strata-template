# Documentation verification outline

Choose checks appropriate to the repository's actual formats and publishing setup:

- Resolve local links and required assets relative to their document or configured site root.
- Check Markdown style against the repository's conventions, including intentional exceptions.
- Check external links separately, so transient network failures can be retried and reviewed
  apart from broken references.
- If the project builds a site, exercise its own build and any meaningful navigation checks.

No linter, site generator, package manager, or runtime is selected here. A Markdown-only hub and a
non-static site need not share a pipeline. Template payloads with downstream-relative links and
placeholders should be checked as rendered fixtures, not mistaken for broken repository docs.
