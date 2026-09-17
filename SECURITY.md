# Security policy

## What this repository is

The index of a twelve-repository portfolio, plus the checker that holds the published pages to a
written specification. It is **not a package**: nothing here is installed, imported, or published
to any registry, and it takes no dependency beyond `pytest`. There is no service to attack and no
release to poison — the realistic reports are about the *record* and about *CI*, not about a
runtime.

## Reporting

**Use GitHub's private vulnerability reporting** — the *Report a vulnerability* button under the
repository's **Security** tab. It opens a channel visible only to the maintainer, which is what a
report should use before anything is public.

Please do not open a public issue for a security report. If private reporting is unavailable to
you, open an issue asking for a private channel and say nothing further in it.

Expect an acknowledgement within a week. This is a personal portfolio maintained by one person, not
a product with an on-call rotation, and an honest slow answer beats a promised fast one.

## What is in scope

- **Anything readable here that should not be** — a credential, a token, a private hostname, or
  personal data in the working tree, in any branch, or anywhere in the history.
  [`docs/audit/0011`](docs/audit/0011_the-pre-publication-security-audit.md) is the audit that
  precedes this repository's visibility change and records what was found; a finding it missed is
  exactly the report this section is for.
- **The GitHub Actions workflow** — `.github/workflows/pagespec.yml`. It declares
  `permissions: contents: read`, uses no secret, has never used `pull_request_target`, and runs on
  GitHub-hosted runners only. Anything that contradicts one of those sentences is a finding.
- **The checker** — `tools/pagespec` parses untrusted HTML and CSS from twelve sibling
  repositories, and under `--fetch` from the live network. It is standard library only and runs in
  CI, so a crafted page that makes it execute something, hang, or exhaust memory is in scope.

## What is not in scope

- **The twelve submodules.** Each is a separate repository with its own issues; report there.
- **The published pages themselves.** They are static GitHub Pages sites owned by those same
  repositories.
- Findings that require write access to this repository, or a compromised maintainer account, to
  exploit.

## A note on the history

The commit history of this repository is part of the record and is deliberately not rewritten for
cosmetic reasons. If you find something in it that should not be readable, that is a report worth
making — the history being intentional does not mean every string in it was.
