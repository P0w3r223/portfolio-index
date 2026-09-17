# The pre-publication security audit

Date: 2026-09-17
Status: accepted
Author: Piotr Cząstkiewicz
Related to: [0010](0010_the-portfolio-audit.md) §3.1 session 13 (the scan of this repository's own
tracked files, of which this is the security half), [0010](0010_the-portfolio-audit.md) §3.2 and §6
(the retired identifier sweep, whose absence this audit had to work around),
[0003](0003_portfolio-review-plan.md) §8 decision 4 and [0004](0004_session1-recruiter-triage.md) §5
(the two sections that name the private repositories §4's R-2 is about)

---

## 1. What this is

A read-only audit of this repository against one question: **what becomes visible the moment its
visibility changes from private to public.** Nothing was modified while it ran, no history was
rewritten, and no finding left the machine.

It is not [`0010`](0010_the-portfolio-audit.md). That audit judges twelve published surfaces as a
recruiter reads them, and its session 13 covers this repository's `tools/`, `tests/`, `docs/` and
root as *presentation*. This one covers the same tree as *exposure*, and the two disagree about
what a defect is: `0010` asks whether a claim is carried, this asks whether a string should be
readable by a stranger.

**The distinction that organises everything below is between the three places a git repository
keeps text**, because a reader who collapses them will reach a false verdict in either direction:

| Layer | What it holds here | Reachable by a stranger after the switch? |
|-------|--------------------|-------------------------------------------|
| `origin/main` | 178 commits, 81 tracked files | yes — and this is the layer everyone checks |
| `refs/pull/*` | **325 commits that are in no branch at all** | **yes**, and no push can change them |
| unreachable objects | local-only residue of rebases and amends | no — they are never pushed, never cloned |

This repository squash-merges, which `CLAUDE.md` already records under a different heading: *a
branch commit is never reachable from `main` and never will be.* The security consequence was not
recorded anywhere until now. Those commits do not disappear — they move to `refs/pull/<n>/head`,
where GitHub serves them to anyone who can read the repository, and where **`git filter-repo`,
`git push --force` and branch deletion all cannot reach.**

## 2. The verdict

**NOT READY.**

Not because of a key — there is no key, and §3 says how thoroughly that was established. Because
three commits reachable from `refs/pull/11` through `refs/pull/36` carry, **in their author and
committer metadata**, a workstation hostname and an internal Active Directory domain belonging to
an employer's network, alongside a personal name that the public identity does not use. Metadata
is not content. No edit to a file removes it, and the two remedies that do work are both decisions
only the owner can take — §6.

Everything else is either repairable in an afternoon (§5, and most of it is repaired by the pull
request carrying this document) or a judgement call about how much of a private working record a
public portfolio index should keep (§4's R-2).

## 3. The method, and what it can and cannot conclude

### 3.1 What was read

Not `git log -p`, and the reason matters. `git log -p` walks commits reachable from the refs you
name, which by construction skips every object that a rebase orphaned. The sweep here read **every
blob in the object database** — `git cat-file --batch-all-objects`, 731 blobs — and mapped each
back to its path and reachability afterwards. That is a strictly larger set than any commit walk,
and it is what found R-9: a blob holding an internal hostname verbatim, reachable from nothing.

Read in full: 731 blobs, 533 commits across every ref including `refs/pull/*` and the reflog, **25
remote-tracking refs under `refs/remotes/origin` — which turned out to be a statement about this
clone and not about `origin`, where there are two branches; §10.1**, 0 tags, 0 stash entries, the
working tree, and the commit messages themselves as a separate corpus.

*Kept with the correction inline rather than silently reduced to two, because the 25 refs really
were read — the sweep's coverage was not smaller than claimed. What was wrong is the label on the
set, and a reader checking this audit's reach deserves both halves.*

### 3.2 What it was read for

**No `gitleaks`, no `trufflehog`, no `git-secrets`** — none is installed and this audit installs
nothing (the repository takes no dependency, and a security audit is a poor place to make the
first exception). The sweep used four hand-built pattern families instead:

1. **High-signal credentials** — roughly thirty shapes: AWS `AKIA`/`ASIA` and `aws_secret_access_key`,
   GitHub `ghp_`/`gho_`/`ghu_`/`ghs_`/`ghr_`/`github_pat_`, Slack `xox*` and `hooks.slack.com`,
   Discord webhooks, Google `AIza` and `ya29.`, `sk-ant-`, `sk-proj-`, bare `sk-`, Stripe live keys,
   SendGrid, npm, PyPI, GitLab `glpat-`, PEM and PuTTY private-key headers, three-segment JWTs,
   Azure `AccountKey=`, Telegram bot tokens.
2. **Credentials inside URLs** — the `scheme://user:pass@host` shape across nine schemes.
3. **Generic assignment** — a secret-looking name bound to a non-trivial quoted literal.
4. **Non-secret but non-public** — e-mail addresses, RFC-1918 and loopback addresses, `.local`
   `.internal` `.corp` `.lan` hostnames, absolute user paths, and Polish identifier shapes
   (PESEL-length digit runs, `PL` IBAN, NIP, phone, card).

Families 1, 2 and 3 returned **zero blobs** across all 731. Family 4 is where §4 comes from.

### 3.3 The three false positives, recorded because a later reader will re-derive them

- **`33857055959`** matches the PESEL shape exactly — eleven digits. It is a GitHub Actions run
  identifier, cited in `0003` §11 and `0006` and verified by reading three lines of context around
  every occurrence. A shape-based sweep for national identifiers will hit this every time it runs.
- **`200 404 500`** in `0009` matches a Polish phone pattern. They are HTTP status codes.
- **This document matches the credential sweep.** §3.2 lists what was searched for, so the strings
  `sk-ant-`, `AIza`, `ghp_`, `xox` and `BEGIN ... PRIVATE KEY` are all present in `0011` itself.
  Re-running the sweep after the move to the published repository returned two blobs, and both
  were versions of this file. *Found on 2026-09-17 while verifying the new repository — and the
  reason it fired there and not in the original audit is instructive: the verification pass used a
  shortened pattern without the length quantifiers (`sk-ant-` rather than
  `sk-ant-[A-Za-z0-9_-]{20,}`). The full pattern distinguishes a token from the name of a token's
  prefix; the short one cannot. The original sweep was right, and the check on the check was what
  was wrong — which is this section's whole subject, arriving one level up.*

A third near-miss is worth more than either. A first pass tested for binary files with
`grep -qa $'\x00'`, which in bash expands to an **empty pattern** — matching every blob in the
repository and reporting all 731 as binary. It was caught only because the answer was absurd rather
than merely wrong. The correct instrument is `git log --numstat`, where a binary file reports `-`
in both columns; it finds **zero binaries in the entire history**. This is
[`failure-classes.md`](../reference/failure-classes.md) territory: *an instrument that cannot fail
is not evidence*, and a sweep that returns "everything" deserves the same suspicion as one that
returns "nothing".

## 4. Findings

Values are masked. **The mask is not decoration.** `git grep` over `origin/main` returns zero hits
for the internal domain in R-1 today; writing it into this document would create, in the file that
reports the exposure, the exposure it reports. §9 says what follows from that.

**R-1 is masked completely rather than symmetrically**, and that is a correction: the first draft
used a four-leading-character mask everywhere, which on an address of the form
`<given-name><surname>@<host>.<domain>` discloses the first four characters of the given name —
*which is R-1's own second finding*. A mask calibrated for a token leaks a name, because the
sensitive part of a token is its tail and the sensitive part of a name is its head. R-3's address
keeps a four-character head because its leading characters name a tool, not a person.

| # | Where | Commit | Type | Risk | In `main`? |
|---|-------|--------|------|------|------------|
| **R-1** | author **and** committer metadata — `…….loc`: personal name, workstation hostname, internal AD domain | `38cb4b2` | internal infrastructure + a second personal identity | **HIGH** | no — but in **26** `refs/pull` refs, `#11`–`#36` |
| **R-2** | **six files**, not four: `0003` §8 decision 4 and §4, `0004` §5, `0002` rows 3.1 and 3.11, `0010` §3.1 row 13c, **`tests/test_entry_state.py`:340, 343, 349** and **`tools/entry_state.py`:297** — four private repositories named, one with size, commit count and last-push date | many | reconnaissance | **MEDIUM** | **yes** |
| **R-3** | `0004` §6.3 line 300 — `biap….com`, a tooling address and not the portfolio's contact route | in `main` | non-public e-mail | **MEDIUM** | **yes** |
| **R-4** | author metadata of two commits, same address as R-3 | `720f4d7`, `d88de42` | non-public e-mail | MEDIUM | no — 26 `refs/pull` refs |
| **R-5** | `0003` §11, `0010` §2 and §4 — the public handle bound explicitly to the legal name | in `main` | PII, almost certainly deliberate | LOW | **yes** |
| **R-6** | `.claude/sessions/2026-09-02.md` — a session brief: branch names, PR numbers, work in progress | pre-ignore | operational detail | LOW | no — `refs/pull` |
| **R-7** | `.idea/*.xml`, `.idea/mad lib.iml` — JetBrains configuration from this repository's first life | early history | noise; no secret, no absolute path | LOW | no |
| **R-8** | `audit-identifiers.local.example` and `tests/test_audit_identifiers.py` — retired 2026-09-11, alive in `refs/pull` | pre-retirement | **verify** | LOW | no |
| **R-9** | blob `ae3ffe77` — a draft of `0008` quoting R-1's domain verbatim | **reachable from no ref** | local residue | **verify** | no |

### 4.1 R-1, and why it is the whole verdict

One commit, `38cb4b2`, dated 2026-08-06, adding a submodule §4.2 declines to name again.
Its author and its committer are both an address of the form
`<given-name><surname>@<workstation-hostname>.<internal-domain>.loc` — the default git identity of a
machine that was never configured, which is exactly how this class of leak is always born.

It is in no branch. `git merge-base --is-ancestor 38cb4b2 origin/main` says no. A reader who stops
there concludes the repository is clean, and that reader is wrong: `git branch -r --contains`
returns **26 pull-request refs**, `#11` through `#36`, and those are served by GitHub to every
reader of a public repository.

Three facts follow, and the third is the one that decides §6:

1. It discloses an **AD domain name and a hostname convention** — reconnaissance material about an
   employer's network, not about this portfolio.
2. It discloses a **personal name the public identity does not use**, correlating two identities
   that are otherwise separate.
3. **No rewrite reaches it.** `filter-repo` rewrites objects you can name from a ref; `--force`
   pushes branches. `refs/pull/*` is read-only and GitHub-owned. This is not a difficulty, it is an
   impossibility, and §6 is built around it.

R-4 is the same shape with a lower severity: a tooling address rather than infrastructure.

### 4.2 R-2, which is a decision and not a defect

`0003` §8 decision 4 does its job honestly — it records *why* a submodule was unpinned, and the
reasoning needs that repository's name to be legible. The cost of that honesty is that
`main` now names four private repositories, one of them with its size, its commit count and the
date of its last push, and one whose name is a Polish phrase describing an internal integration.

Under the private-repository assumption every one of those sentences was correct. The assumption is
what is changing. **This is the only finding in §4 that is a genuine trade-off** rather than
something to fix: redacting it costs the record its reasoning, and `tests/test_entry_state.py:340`
asserts on one of the names, so a blind text substitution reddens the suite. §6 step 2 gives both
routes with that cost priced in.

### 4.3 What is clean, stated positively

Across 731 blobs and 533 commits: no AWS, GCP, Azure, GitHub, Slack, Discord, npm, PyPI, GitLab,
Stripe, SendGrid, OpenAI or Anthropic credential of any shape; no PEM or PuTTY private key; no JWT;
no connection string and no credential in any URL; no `.env`, `.pem`, `.key`, `id_rsa` or `.netrc`
by name or by content; **no `secrets.` reference in any version of any workflow, ever**; no private
or loopback address; no internal hostname in any *tracked* file; no binary file in the entire
history; and no national-identifier, IBAN, NIP or payment-card value.

## 5. Repository hygiene

| Item | State |
|------|-------|
| `.gitignore` | **exemplary** — scoped rather than blanket, every rule carrying the finding that produced it |
| `LICENSE` | **absent by decision, 2026-09-17** — all rights reserved, which is what a working record should say. `0001` §6 and `0002` row 3.11 hold *other* repositories to having one; §6 step 4 names that inconsistency and keeps it deliberately |
| `SECURITY.md` | absent — added by this pull request |
| `CONTRIBUTING.md`, `CODEOWNERS`, `CODE_OF_CONDUCT.md` | absent — see §5.1 |
| `README.md` | **self-contradicting on the switch** — its third paragraph says this repository *is private* and explains what follows from that |
| `CLAUDE.md` | **the same, and it is read first** — line 7 opens "The **private** index", and the "public landing surface" paragraph is an *argument resting on* that premise, not merely a stale date. Both now carry the condition rather than a rewrite, because route A leaves this repository private |
| `0004`, `0008`, `0009` | assert privacy too, and are covered by the `README.md` note: they are dated records under `docs/audit/` and are not retrofitted |
| Large / binary files | none; the largest object is `0008` at 274.6 KiB (281 187 bytes) of markdown, `size-pack` 2.01 MiB |
| `permissions:` | **present**, `contents: read`, workflow-level |
| `pull_request_target` | never used |
| Third-party actions | `actions/checkout@v7` and `actions/setup-python@v7`, **pinned to a tag, not a SHA** |
| Runners | `ubuntu-latest` only; no `self-hosted` |
| Stale branches | ~~23~~ ~~25~~ — **none. `origin` holds two branches: `main` and `archive/legacy-games`.** This row was wrong twice, and §10's sixth entry is why the second way is worse than the first |
| `archive/legacy-games` | its README links to a `master` branch that does not exist, and `hangman.py` contains tic-tac-toe |

### 5.1 What this pull request adds, and what it deliberately does not

Added: this document, `SECURITY.md`, and the `README.md` correction.

**Not added: `LICENSE`, `CONTRIBUTING.md`, `CODEOWNERS`.** A licence is a legal declaration about
who may use this record and on what terms, and the twelve siblings are not a precedent worth
applying blind — `it-job-radar` carries MIT *with* a `NOTICE` carving `docs/data/` out of the grant,
precisely because a blanket MIT said something its owner had not meant. The choice was the owner's,
and **it has been made: no licence** — §6 step 4 records it as a decision, with the inconsistency
against `0001` §6 named there rather than left for a reader to find.
`CONTRIBUTING.md` and `CODEOWNERS` describe a collaboration
model that does not exist here; `SECURITY.md` is different, because it names a reporting channel a
stranger will look for.

## 6. The repair, in the order the steps must happen

### Step 0 — the decision the rest depends on

`refs/pull/*` cannot be rewritten. Two routes reach a clean public artefact, and they cost
different things.

| | **A — a clean repository** | **B — this repository, plus Support** |
|---|---|---|
| Method | fresh single-branch clone of `main`, pushed to a new public repository | `filter-repo` on `main`, force-push, then a Support request |
| R-1, R-4 | **solved by construction** — a clone never fetches `refs/pull` | needs manual intervention, on no guaranteed timetable |
| Cost | loses 140 pull requests, issues, stars | keeps everything |
| Certainty | high, and verifiable locally before pushing | depends on a third party |

**Recommended: A.** The pull-request history is a working record, not a portfolio asset, and the
private repository can be kept intact as the archive. The verification is two commands:

```bash
git clone --branch main --single-branch \
  https://github.com/P0w3r223/current_projects.git cp-public
cd cp-public
git log --all --format='%ae%n%ce' | sort -u     # expect only the public identity and GitHub's noreply

# after pushing, against the NEW remote — this is the one that proves anything:
git ls-remote https://github.com/P0w3r223/<new>.git 'refs/pull/*'   # expect no output
```

*The first draft checked `git for-each-ref | grep -c 'refs/pull'` inside the fresh clone and
expected 0. **That command cannot fail.** No clone fetches `refs/pull` without an explicit
refspec — this repository's own `refs/remotes/pr/*` came from a one-off audit fetch — so it prints
`0` for a clone of any repository, cleaned or not. It could not tell the outcome it checked for
from its opposite, which is §3.3's standard applied to this document's own verification, and it was
caught by review rather than by writing it. The claim that needs proving is server-side, which is
what `ls-remote` asks. (`grep -c` also exits 1 on zero matches, so it must not sit in a `&&` chain —
the same trap, one layer down.)*

### Step 0 was taken on 2026-09-17, and this repository is its output

**Route A, executed.** `portfolio-index` is a clone of `current_projects`'s `main`, and the
original stays private with its 142 pull requests intact. What the remedy actually delivered,
measured against the new remote rather than against a local clone — §10.1's rule applied to the
repair itself:

| Check | Result |
|-------|--------|
| `git ls-remote <new> 'refs/pull/*'` | **empty** — the layer §1 is about does not exist here |
| Refs on the server | `HEAD` and `refs/heads/main`, nothing else |
| Author *and* committer over all 182 commits | the public identity and GitHub's noreply, nothing else |
| R-1's three literals across 441 blobs | **zero** — and this row named them in its first draft, which §9 rule 1 forbids and §3.3 predicts: a line reporting *no match* became one |
| R-2, R-3 | present, on the owner's decision of the same day |

**R-1 and R-4 are gone, and not because anything was deleted** — a clone never fetched them.
That is the whole argument for route A over a rewrite, and it is the one claim in this document
that was verified twice: once in the clone before pushing, once against the server afterwards.

**Four files needed the move, and two were code.** `tools/entry_state.py`'s `INDEX` is what the
pull-request query asks GitHub about; left at the old name, every open pull request here would
file as *outside the portfolio* — the 2026-09-07 misreading, which `tests/test_entry_state.py`
exists to mechanise against. **The audit did not find this.** It swept for secrets and for
non-public data, and a dependency on the repository's own name is neither. A move is not a
publication, and this document had only planned the publication.

### What step 1 caught, which is the finding of the repair

The identity in the fresh clone was **empty**. `user.email` was set *locally* in the original
repository and never globally, so every new clone starts unconfigured and git falls back to the
machine's default — `<user>@<hostname>.<internal-domain>`. **That is the exact mechanism behind
`38cb4b2`**, and it would have re-created R-1 in the first commit of the clean repository if the
identity had not been checked before committing.

So step 1 is not cleanup after an incident. It is switching off a live cause, and the audit had
it ranked below the move. Corrected here: **check `git var GIT_AUTHOR_IDENT` in any fresh clone
before the first commit** — it prints what git would actually write, which `git config user.email`
does not when the value is absent. `user.useConfigOnly true` makes the failure loud instead.

### Two notes on the settings pass

- **Required status checks were missing from the hand-off instructions**, though §7 lists them.
  A ruleset with `pull_request` but no `required_status_checks` merges a red pull request without
  complaint. Added after the fact, pinned to `checker (no submodules)` and
  `checker over the published surfaces` — deliberately not `the live surface`, which reports
  `skipped` outside its schedule, and not the dynamic `update-pip-graph`.
- **Enabling Dependabot adds a workflow.** GitHub starts a managed `Dependency Graph`
  (`dynamic/dependabot/update-graph`) run, which appears as a check named `update-pip-graph`
  and is in no file in this repository. Harmless, and worth knowing before someone greps the
  tree for it.

### Step 1 — stop the source, then treat the disclosure as permanent

Nothing here is a credential, so nothing rotates in the cryptographic sense. The rule that anything
reaching history is compromised applies to *information*: the internal domain and hostname
convention in R-1 are disclosed to everyone who has had read access, and un-publishing them later
changes nothing about that.

Fix the machine that produced `38cb4b2`, or it recurs:

```bash
git config --global user.name  "P0w3r223"
git config --global user.email "p0w3r2243@gmail.com"
git config --global user.useConfigOnly true   # refuse a commit from an unconfigured identity
```

Whether the AD domain disclosure warrants telling that network's administrators is the owner's call
and outside what this audit can decide.

### Step 2 — R-2 and R-3, if they are to leave `main` at all

Only under route B, and only if §4.2's trade-off is resolved toward redaction. **`filter-repo` with
`--replace-text` will redden `tests/test_entry_state.py:340`**, which asserts on one of the names;
repair it in the same pass or the suite fails on the first run after the rewrite.

```bash
python -m pip install git-filter-repo
git clone --no-local https://github.com/P0w3r223/current_projects.git cp-clean
cd cp-clean
git filter-repo --replace-text ../replacements.txt   # one `literal==>replacement` per line
git grep -c '<each literal from that file>' $(git rev-list --all) 2>/dev/null | wc -l   # expect 0
```

The replacement file holds R-2's four repository names and R-3's address as literals. It is written
at repair time and **not committed** — §9 rule 2 is why a document that redacts those names cannot
also ship a file listing them.

### Step 3 — the consequences, under route B only

1. Every SHA changes. `git push --force --all && git push --force --tags`.
2. Every existing clone must be re-cloned. A `pull` across a rewrite produces a divergence no merge
   resolves, and the twelve submodule gitlinks make the failure mode confusing rather than obvious.
3. **Ask GitHub Support to purge cached commits and pull-request views**, naming `38cb4b2`,
   `720f4d7` and `d88de42` and the range `refs/pull/11`–`refs/pull/36`.
4. **Change visibility only after Support confirms.** The other order opens a window in which
   everything is public and nothing is cleaned.

### Step 4 — open, and the owner's to close

- ~~**`LICENSE`**~~ — **closed 2026-09-17: no licence, and that is a decision rather than an
  omission.** No `LICENSE` file means all rights reserved, which is what this repository should
  say: it is a working record, not code anyone is meant to reuse, and the portfolio's reusable
  half lives in the twelve siblings, which carry their own licences. **The inconsistency is
  acknowledged rather than discovered later**: `0001` §6 and `0002` row 3.11 hold *other*
  repositories to having a `LICENSE`, and this one now knowingly does not — those rows were
  written about published project code, and the audit record is a different kind of artefact.
  Recorded here because an unlicensed repository is indistinguishable, from the outside, from one
  whose owner forgot; a later reader finding no `LICENSE` should find this sentence instead of
  re-opening the question.
- **R-2** — redact, or accept as the price of a record that explains itself.
- ~~**The 23 stale branches**~~ — **closed 2026-09-17: there were none.** `origin` holds `main`
  and `archive/legacy-games`, and has for some time. Nothing to delete, so the
  `gh api -X DELETE` this bullet used to carry is gone with it. **The instrument is
  `git ls-remote --heads origin`**, which asks the server. The
  `git for-each-ref refs/remotes/origin` this bullet recommended one revision ago reads the
  *local remote-tracking cache*, and `git fetch --all` does not prune it — so 23 branches deleted
  from `origin` weeks ago were still sitting in this clone, and the audit counted them. §10's
  sixth entry is the class.

## 7. The GitHub checklist

None of this is reachable from code, and all of it belongs **before** the visibility switch.

**`Settings → Code security and analysis`**
- [ ] Secret scanning → Enable
- [ ] **Push protection** → Enable — the only control here that prevents rather than reports
- [ ] Dependabot alerts → Enable
- [ ] Dependabot security updates → Enable
- [ ] Private vulnerability reporting → Enable

**`Settings → Rules → Rulesets → New branch ruleset`**, target `main`
- [ ] Require a pull request before merging, with 1 approval
- [ ] Require status checks: `checker (no submodules)`, `checker over the published surfaces`
- [ ] Require branches to be up to date before merging
- [ ] **Block force pushes** · **Restrict deletions**
- [ ] Require linear history — this repository already squash-merges
- [ ] Require signed commits — needs GPG or SSH signing configured first

**`Settings → Rules → Rulesets → New tag ruleset`**
- [ ] Restrict creations, updates and deletions — there are 0 tags today, which is the cheapest
      moment to set this

**`Settings → Actions → General`**
- [ ] Workflow permissions → **Read repository contents permission**
- [ ] Clear *Allow GitHub Actions to create and approve pull requests*
- [ ] Fork pull request workflows → **Require approval for all outside collaborators**
- [ ] Actions permissions → Allow select actions → `actions/*`, or a SHA allowlist

**Access review — each line separately**
- [ ] Collaborators and teams
- [ ] **Deploy keys** — a write-capable key becomes a target the moment the repository is public
- [ ] **Webhooks** — a URL pointing at an internal endpoint discloses infrastructure
- [ ] Integrations / GitHub Apps — installed scopes
- [ ] Secrets and variables → Actions, **and the Environments tab** — no workflow here uses one;
      delete anything left over

**Account and surface**
- [ ] Enforce 2FA
- [ ] `Settings → General → Features` — disable Wiki, Discussions, Projects if unused
- [ ] `Settings → General → Forks` — decide
- [ ] `Settings → Pages` — this repository publishes no page; confirm it stays off
- [x] ~~Confirm all twelve submodules are public~~ — **done 2026-09-17, all twelve.** Kept as a
      ticked line rather than deleted, because this is the item a later reader will re-derive, and
      the answer has a date on it

## 8. What could not be verified, and why

1. **Whether blob `ae3ffe77` (R-9) exists on GitHub's side.** Locally it is reachable from nothing,
   so it is never pushed and never cloned. But GitHub retains objects orphaned by force-pushes and
   serves them by direct SHA. Settling it means querying the API, which would mean sending a finding
   to a third party — the one thing this audit was told not to do. **It is the only blob whose
   content quotes R-1's domain verbatim.** Treat it as possibly reachable.
2. **No `gitleaks` and no `trufflehog`.** §3.2 says what replaced them. A shape nobody anticipated
   could have survived; run one as an independent check before the switch.
3. **Whether the public contact address is already public.** R-5 is rated LOW on the assumption
   that it is the portfolio's deliberate contact route. If that is wrong, R-5 is MEDIUM.
4. ~~**Whether the four repositories named in R-2 are still private.**~~ **Settled 2026-09-17, and
   it does not help.** All four answer `private: true`. R-2 stands at MEDIUM exactly as rated —
   the check could only have lowered it, and did not.
5. ~~**Whether the twelve submodules are public.**~~ **Settled 2026-09-17: all twelve are.** So
   `.gitmodules` discloses nothing a stranger cannot already reach, and `git clone --recursive`
   works anonymously. Their *contents* are still out of scope — separate repositories, each
   needing its own pass, which is `0010` §3.1 sessions 1–12.
6. **Everything in §7.** Permissions, deploy keys, webhooks and Actions secrets are invisible from
   the tree, which is why §7 is a checklist and not a verdict.

## 9. What this document does to itself

A security report is a document about strings that should not be read, which makes it the easiest
possible place to write those strings down. Three rules were applied while writing it, and they are
recorded because the next such report will face the same pressure:

1. **R-1's domain and hostname appear nowhere above.** `git grep` over `origin/main` returns zero
   hits for them today. Quoting them here would put them in `main` for the first time — and a
   finding is not closed by a document that reproduces it. The mask is load-bearing, not cosmetic.
2. **R-2's names are cited by section, not repeated.** They are already in `main` in four documents,
   so a fifth changes nothing about the exposure — but it would add a fifth site to redact if §6
   step 2 is ever taken, which is the fan-out shape `0010` §5 records from the amended-ADR finding.
3. **The commit SHAs are quoted in full**, deliberately, and so is the public contact address in
   §6 step 1. The SHAs are needed verbatim for the Support request in §6 step 3, they disclose
   nothing on their own, and a masked SHA is useless to the one reader who has to act on it. The
   address is R-5, rated LOW because it is the portfolio's published contact route — masking a
   value whose whole purpose is to be read would be theatre.

**All three rules were broken in this document's first draft, and a grep for its own masks is what
caught them.** Rule 2 failed twice — once in a quoted commit subject, which is the site no reader
thinks of as content, and once in prose explaining §4.2's trade-off, where naming the repository
felt like precision. Rule 1's literal survived only because it was never typed. The lesson is not
that care was insufficient; it is that **a redaction rule needs an instrument, exactly like every
other claim in this repository** — the grep runs in seconds and found in one pass what a careful
re-reading had already missed. If this document is ever extended, run it again first.

*The tension in rule 1 is real and worth naming: a masked finding is harder to act on than a quoted
one. It is accepted here because the owner can read the unmasked value out of `git log` in one
command, and a stranger cannot read it out of this file at all — which is the asymmetry the whole
audit is about.*

## 10. What the review of this document found

A `code-reviewer` pass over the first commit confirmed every load-bearing security claim against
the object database — 325, 26, the `--is-ancestor` answer, both action SHAs, the §9 greps. **It
then found five defects, and not one of them was in the security analysis.** All five were in the
*pointers and counts* — the part a reader acts on:

| What | Shape |
|------|-------|
| `CLAUDE.md` asserts privacy at line 7, outside the `README` note's scope | the fix repaired the file a reader opens second and missed the one they open first |
| "25 stale branches" | **the count of all branches.** `%(refname:short)` renders `refs/remotes/origin/HEAD` as plain `origin`, so a filter matching `origin/HEAD` misses it — and the `gh api -X DELETE` beside the number would have deleted `archive/legacy-games` |
| §6 step 0's first verification | **a command that cannot fail** — §3.3's own standard, violated two sections later |
| R-3 cited `0004` §5 | right line, wrong section; `tools.citations` reports `unresolved 0` because §5 *exists*. The resolver checks that a named section exists, never that it holds what the citing line says |
| R-2 named four documents | the string is in **six** files — `tests/test_entry_state.py` and `tools/entry_state.py:297` are code, and §9 rule 2's own wording ("in `main` in four documents") is what made them easy to drop |

Three things follow, and the third is the one worth carrying:

1. **Two of the five sat on commands that delete or that prove a remedy worked.** A wrong number
   in prose is a correction; a wrong number wired to `-X DELETE` is an incident.
2. **`tools.citations` has a blind spot with a name now.** It answers *does this section exist*,
   not *does it hold this*. Every `unresolved 0` in this repository's history carries that caveat,
   and R-3's defect is the first recorded instance of it mattering.
3. **The battery could not have found any of these, and the review found all five** — the second
   time a `code-reviewer` pass has caught a class the mutation battery is structurally blind to
   (`0010` §5 records the first). A document has no mutants. What it has is claims, and the only
   instrument that reads a claim against the thing it describes is another reader.

### 10.1 The sixth, found after the merge, and it is the one that matters

**The stale-branch row was wrong a second time, and the second way is worse.** It said 25, the
review corrected it to 23, and both numbers are fiction: `origin` holds **two** branches, `main`
and `archive/legacy-games`. There was never anything to delete.

The first error was a bad filter. The second was reading the wrong thing entirely. Every count
came from `git for-each-ref refs/remotes/origin` — the **local remote-tracking cache**, which is
not `origin`. Branches deleted from the server weeks ago sit in a clone indefinitely, because
`git fetch --all` does not prune. It was found only when `git fetch --prune` ran as part of
cleaning up after the merge, and printed the deletions of branches this audit had listed as
present.

Three things make this the most useful entry in the document:

1. **It is the audit's own central finding, turned around.** §1's whole argument is that a
   repository keeps text in layers, and that the layer a reader checks locally is not the layer
   that decides. The stale-branch row failed for exactly that reason, in the document making the
   argument. The `refs/pull/*` analysis was correct because it was verified against `origin`;
   this row was not, and nothing in the method distinguished them.
2. **`CLAUDE.md` warns about this, in its last section, in these words**: *`origin/main` is a
   local file a session inherits and nothing refreshes on its own.* That section exists because
   two sessions reached the same false conclusion from a stale ref on 2026-09-07. This is the
   third, and the first to survive both a review and a merge.
3. **The review confirmed 23 — because it read the same cache.** A second reader is not an
   independent instrument when both readers query the same stale source. §10's own conclusion
   ("the only instrument that reads a claim against the thing it describes is another reader")
   needs that qualification: *against the thing it describes*, not against the same local copy of
   it. The correction is not "get a reviewer", it is **name the source each figure came from**,
   and prefer the one that can answer for the server.

The mechanical rule that follows, and it is cheap: **`git ls-remote` for anything that is a claim
about `origin`.** `for-each-ref` answers a question about this clone, which is a different
question and almost never the one being asked.
