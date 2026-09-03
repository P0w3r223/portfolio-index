# Session 1 — Recruiter Triage

Date: 2026-09-02 (revised the same day after an adversarial verification pass — see § 6).
**Reconciled 2026-09-03** against the repositories and the account: §5's `infra-docker-workmate`
decision, §4's `apply-scout` caption, §9's parquet bullet, §3.4's pins and §6.1's contact fields
had all been superseded and none of them said so. The rule that catches this, and why one document
is not the record, is `0003` § 9.
Status: accepted
Author: P0w3r223
Related to: [0003_portfolio-review-plan.md](0003_portfolio-review-plan.md) § 3 and § 9, `README.md`, the profile README

---

## 1. What this session had to answer

From the plan's session table: *rank all 13 repos by 60-second recruiter value; keep, demote to
Level B, or cut; name the gaps in the stack for AI Engineer and Data Scientist.* Both roles are
weighted equally, and the plan put everything on the table — including demoting the flagship.

## 2. Method, and why it looked at the pages first

A recruiter with sixty seconds does not read a README. They open a link. So the ranking is built
from what the **published page** says in its first line, checked against what the project actually
contains — not from the index's own description of itself, which is the thing under review.

Two indexes exist and only one is public. `current_projects` is **private**, so its Level A / B / P
tables are invisible to any reader. **The public index is the profile README**, 45 lines. Every
statement below about "what a recruiter sees" means that file and the pages it links.

## 3. Four findings that decided the ranking

### 3.1 The public index does not mention its strongest project

`doc-extract` appears **nowhere** in the profile README — not in *Start here*, not in *Live demos*,
not in *Also on the profile*. Verified against the whole 45-line file, not a truncated read.

It is the most substantial artifact in the portfolio: **823 tests collected** (806 passing, 17
skipped — the repository's own `CLAUDE.md` counts the passing ones), six milestones closed and
eleven sub-milestones of the seventh, **two** ADRs, a measured injection suite, a vision path, and a
genuine finding about a national standard — the Ministry's KSeF FA(3) XSD is 183 798 bytes carrying
328 enumerations and **zero assertions**, so *net + VAT = gross* is unenforced by Polish law's own
schema. That is the sort of thing an interviewer remembers.

*Two figures here were wrong in the first draft of this document and are corrected above.* It said
"806 tests" without saying which count that was, and "six ADRs" — six were **identified** during
the design session; two are written. The eleven sub-milestones are real (`M7a`–`M7k` in the
repository's own table), but its prose one line above that table says "ten", so the repository
contradicts itself and should be fixed there.

A reader of the profile cannot reach it.

### 3.2 The presentation is inverted against the ranking

What the `h1` of each published page says:

| project | first line a visitor reads |
|---|---|
| `ab-lab` | *A 5% test is only 5% if you look once, count each user once, and test one metric* |
| `it-job-radar` | *Most junior IT offers in Poland are not development jobs* |
| `auth-log-scan` | *108 failed logins in 7.1 hours — and only some of them are an attack* |
| `doc-extract` | *Poland's national e-invoice schema checks nothing an accountant would* |
| `car-price-ml` | *A 13.9 MB model prices this market better than a 590 MB one* |
| `pl-review-sense` | *HerBERT reaches 0.986 against the baseline's 0.944* |
| `wroclaw-air-insights` | *Live 24-hour PM2.5 forecast* |
| `mini-traceroute` | *A traceroute, one TTL at a time* |
| **`apply-scout`** ⭐ | **`apply-scout`** |
| **`mlops-car-price`** | **`mlops-car-price`** |
| **`pl-jobs-lora`** | **`pl-jobs-lora`** |

The three projects the index sells hardest — the flagship among them — open with a repository name.
A Level B side project opens with a measured finding. This is not a matter of taste at sixty
seconds: it is the difference between *this person established something* and *this is some repo*.

It matches the family split the plan already recorded, and confirms that split is not cosmetic:
family B is exactly the three headline projects.

### 3.3 The index understates its best project by four milestones

`README.md` gives `doc-extract` the status **`🚧 M2 of 7`** and says *"milestones 3–7 … are not
built"*. The repository's README, its `CLAUDE.md` and the page eyebrow all say **"milestones 1–6 of
7, and most of the seventh"**. The page's own KPI tile says **`5 / 7`**.

So **three** distinct figures across six surfaces, and the one a recruiter reads first is the
lowest — four milestones below what the project has. A portfolio whose central claim is *measured
rather than asserted* cannot publish three numbers for one fact.

*Corrected:* the first draft said "four different numbers" and "a factor of four". `0003` said
three and was right; this document inflated it by counting `CLAUDE.md` separately when it agrees
with the eyebrow.

### 3.4 Two hygiene facts on the repository cards

`doc-extract` carries **zero topics**, against 6–14 on every other repository, and ~~has **no
authored CI** — 806 passing tests that run on no push~~. (GitHub's implicit
`pages-build-deployment` workflow does run, so "no CI at all" overstates it; there is no test or
lint workflow. The other eleven repos each have one, green on `main`.) **The CI half closed
2026-09-03**, `doc-extract#6` — 806 passed, 22 skipped, `ruff` clean, on `push` and
`pull_request`. All twelve public repositories now run a test job, verified by reading every
workflow file rather than by listing repositories, which is the mistake that produced the
original false all-clear. **The zero topics stand**, and stay with Session 2.

`car-price-ml` reports its primary language as **Jupyter Notebook**, which says "notebooks" about a
project with a FastAPI service and a Docker image. That one **is** on a pinned card.

*Corrected:* the first draft called both facts "visible on the pinned cards". `doc-extract` **is
not pinned** — the six pinned repos are `ab-lab`, `apply-scout`, `car-price-ml`, `it-job-radar`,
`mlops-car-price`, `wroclaw-air-insights`. Which is itself the point of §3.1 restated: the project
this session promotes to flagship is neither pinned nor mentioned.

*Added 2026-09-03, because "pin it" turns out not to be a free action.* **All six slots are full**
— re-read from the GraphQL API, the list above is unchanged — so pinning the flagship means
unpinning something. The recommendation is **`car-price-ml`**, for two reasons that point the same
way: the portfolio currently spends **two of its six pins on the same dataset** (`car-price-ml` and
`mlops-car-price` are both the car-price problem), and `car-price-ml` is the one whose card
actively misreports the project — *Jupyter Notebook*, per this section. Neither demoted project is
pinned, so the demotions free nothing; this is a swap between two Level A projects or it does not
happen. Pinning is an account setting with no public API, so it is the author's action.

**Done, as recommended.** Read back from the API 2026-09-03: `doc-extract, ab-lab, apply-scout,
mlops-car-price, wroclaw-air-insights, it-job-radar` — `car-price-ml` swapped out. *So the
flagship is pinned and the second sentence of §3.4 above is now history rather than a finding.*
`car-price-ml`'s misreported language stays open on its own account (Session 2); it is simply no
longer on a pinned card.

## 4. The ranking

Ordered by what sixty seconds buys a reader hiring for AI Engineer or Data Scientist.

| | project | reads for | verdict |
|---|---|---|---|
| 1 | **ab-lab** (P2) | DS | **keep — the Data Scientist headline.** A falsifiable claim, three independent routes to it, two of them derived on paper before the code existed. `statsmodels` used only as a test oracle |
| 2 | **doc-extract** (P5) | AI Eng | **keep — the AI flagship.** The strongest engineering here, and today invisible |
| 3 | **it-job-radar** (A2) | DS / DE | **keep.** 39 % of adverts are one role republished city by city — which had put azure third in the demand ranking instead of seventh. A real finding produced by the data work itself |
| 4 | **car-price-ml** (A3) | DS | **keep.** Full cycle, model running in the reader's browser, and it refuses the cars it cannot price rather than guessing |
| 5 | **apply-scout** (P3) | AI Eng | **keep, loses the ⭐.** The evaluation harness holds up — 194 tests, and CI replays the expected tables byte-identical. The presentation is the worst in the portfolio, the loop carries an unnamed security debt, and ~~**the page still contradicts itself in public**: its table reads 62 % completion and the caption beneath it still reads 75 %~~ — **closed by `#23`**, verified live: table and caption both read 62 % |
| 6 | **mlops-car-price** (P1) | AI Eng / MLOps | **keep.** A drift detector that is itself measured, promotion by paired bootstrap. Family B presentation |
| 7 | **wroclaw-air-insights** (A1) | DS | **keep.** The one piece of evidence in the portfolio fixed *in advance* of its outcome — though a page reader cannot see that (§ 6.4). Weak `h1`, **no licence**. It does have four KPI tiles; `0003`'s "no KPI tiles" was wrong, and it uses a third naming convention (`.stat`) rather than lacking them |
| 8 | **auth-log-scan** (B2) | — | **keep at Level B.** Its page is better than the flagship's; the subject is not the target role |
| 9 | **pl-jobs-lora** (P4) | AI Eng | **keep.** Sound after the metric corrections; family B presentation |
| 10 | **pl-review-sense** (A4) | NLP | **demote to Level B** — see §5 |
| 11 | **mini-traceroute** (B1) | — | **keep at Level B.** C++ breadth, cheap to hold |
| 12 | **token-budget** (A6) | — | **demote to Level B** — see §5 |
| 13 | **studia-rag** (A5) | — | **struck** — see §5 |

## 5. Decisions taken

### The flagship moves

**`doc-extract` becomes the AI Engineer flagship; `ab-lab` becomes the Data Scientist headline.
`apply-scout` remains a strong P3 and loses the ⭐.**

Two roles weighted equally is two headlines, not one. A recruiter hiring a Data Scientist who lands
on an LLM agent has been shown the wrong thing, however good it is.

`doc-extract` over `apply-scout` on the merits: it is larger, more finished, carries a result rather
than a capability, and — decisively — it treats untrusted input as an **explicit threat model**
(lethal trifecta leg [A] only, document text delimited as data with a fence the document cannot
forge, a grounding check, and a measured attack-success-rate suite). That is the exact weakness
`apply-scout` has, and all three legs verify in its source: `read_cv.py` takes a free path string
with no base-directory join or `resolve()`; `fetch.py` fetches any URL with redirects followed, no
scheme check, no host allowlist and no loopback guard; the fetched content goes back to the model.
Its README's **eighteen**-item limitations list does not name any of it, and neither the README nor
`CLAUDE.md` contains the words injection, untrusted, SSRF, allowlist or path traversal.

`apply-scout` was **not** demoted. "An LLM agent written from scratch" is the most legible category
in the portfolio for an AI Engineer reader, and the harness behind it is real. It keeps its place;
it stops being the single thing the portfolio points at.

### Struck

**A5 `studia-rag` is removed from the index.** There is no repository — the row is an announcement
typeset like a shipped project, which `0001` already flagged. Nothing to delete but the row. If one
row promises something that does not exist, a reader is entitled to doubt the others.

The RAG idea itself is not dropped; it returns as a Session 2 proposal with a scope and a budget.

### Demoted to Level B

**A6 `token-budget`** — the only project with no visual representation at all, which breaks the
plan's own end state (*a project with no page is not finished*). Rather than build it a page for a
stdlib CLI that proves nothing the other twelve do not, it moves to Level B, where a small proof is
what the tier is for. The rule stops being broken because the tier no longer promises an exhibit.

**A4 `pl-review-sense`** — TF-IDF against HerBERT on PolEmo 2.0 is a textbook exercise. Done
properly, but it distinguishes nothing, and standing in Level A it implies a textbook exercise is
one of the portfolio's pillars. Page and repository are untouched.

*Recorded against this one:* it is the only purely NLP project here, and HerBERT/PolEmo is a
specific Polish-language competence nothing else demonstrates. The demotion is a presentation
judgment, not a claim that the work is weak.

### Considered and not taken

~~**`infra-docker-workmate` stays a submodule.** Proposed for removal — private, absent from the
index, Polish description against the convention, 200 commits behind its own origin — and declined.
It remains an item nobody reading the portfolio can see, and it is still drifting.~~

**Reversed 2026-09-03, and unpinned by `#42`** — §9 records why, and this is where a reader looks
for the decision. The proposal had been to move its contents somewhere safe; the survey found
there is nowhere to move them *to*, because they already live in their own private repository. So
the submodule link is the only thing removed and the repository is untouched.

## 6. What this triage missed, found by verifying it

An adversarial verification pass was run over this document and `0003` after the ranking was
settled. It confirmed every structural finding above, and found four things about the
recruiter-facing surface that four audit documents had never looked at. They are recorded here
because they bear on the same question this session was asked, and two of them outrank items the
plan is already carrying.

### 6.1 A recruiter has no way to make contact

Checked against the GitHub API: `name` is null, `bio` is null, `email` is null, `blog` is empty,
`hireable` is null, and there are **zero social accounts**. The 45-line profile README carries no
email address, no LinkedIn, no CV link. The only identifier anywhere is the first name in its `h1`.

Four documents about a recruiter with sixty seconds, and none asked what that recruiter does when
they are convinced. The profile renders as the bare handle `P0w3r223` with an empty bio. Every
other improvement in this review raises the probability of a reader wanting to make contact, and
none of them gives them a way to.

This is the cheapest high-value item identified in the entire review.

**Half closed 2026-09-03, by the author.** Re-read from the API: `email` is
`p0w3r2243@gmail.com`, `bio` is set, the URL field points at the `doc-extract` live site, and
*Available for hire* is on. What is still open, and why the other half is not the author's:

- ~~`email` null~~, ~~`blog` empty~~, ~~`hireable` null~~ — **set**.
- **`name` is still null**, so the profile still renders as the bare handle. An account field.
- **The bio as published reads *"Open to AI/ ML engineer"*** — a stray space and a truncated final
  clause, against the agreed *"Open to AI/ML engineering roles."* An account field.
- **The 45-line profile README still carries no contact line.** The address reached the sidebar
  and not the index, and a reader working down the README need never look at the sidebar. This one
  is a *file*, so it is not blocked on the account at all — which is why §8 below moves it out of
  "ahead of all of them, and the author's" and into the work queue (`0003` §9).

### 6.2 Commit metadata

See §6.3.

### 6.3 The new flagship's commits are not credited to the account

**37 of `doc-extract`'s 40 commits** are authored from a second account of mine, an address not
registered on the GitHub account. The API returns `author: null` for them: no avatar, no profile
link, and **no credit in the contribution graph**. Every other repository uses the registered
address.

This is on the repository §5 promotes to AI Engineer flagship. A reader who opens its history sees forty commits, thirty-seven of them from nobody.

### 6.2 + 6.3 resolved

The
history of all thirteen repositories was rewritten with `git filter-repo`. Three stray identities — including the two this triage never saw, `Piotr Cząstkiewicz` and a
machine hostname — were folded onto the registered address. `doc-extract` is now credited to the
account for all of its commits, and the *cause* was a local `user.email` in that one repository's
config, so it cannot recur. Verified against mirror backups taken first: every commit pairs
1:1 with identical tree, dates and parents.

A rewritten commit invalidates its signature, so the rewrite
stripped every one: **153 commits carried GitHub's signature before it and 4 do now** — the four
merges made since. Roughly a hundred and fifty public merge commits lost their *Verified* badge,
and nothing brings them back. It bought the consistency this section is about, and a portfolio
arguing about provenance should say what the consistency cost rather than let a reader notice the
missing badges on their own.

### 6.4 The three most-promoted pages have no social metadata, and A1's best claim is invisible

`apply-scout`, `mlops-car-price` and `pl-jobs-lora` carry **no `meta description`, no `og:*`, no
`twitter:*` and no favicon**. Pasting the flagship's link into LinkedIn, Slack or an email produces
a bare URL with no preview card. Their `<title>` also leads with the repository name, so the
inversion §3.2 found in the `h1` extends to the search-result line. No page anywhere carries an
`og:image`, so even the eight well-formed pages produce text-only cards.

Separately: `wroclaw-air-insights`'s forecast log is genuine — a branch with 767 rows, written
before each hour exists — but the grading step runs `continue-on-error` and prints only into CI
logs. **The published page contains no occurrence of "logged" or "graded" and no prospective
score.** The reason §4 gives for keeping A1 is true of the repository and absent from the artifact a
recruiter opens.

### 6.5 The table-wrapping generalisation was never applied to the pages it predicted

`0003` closed its fix track having correctly diagnosed "one gap in the pattern family A's pages are
generated from" — then fixed four pages. Measured on the live sites: `pl-review-sense` has **seven
tables and zero wrappers**, `it-job-radar` one and zero, `mini-traceroute` two and zero. They do not
overflow today only because they happen to be narrow enough, which is precisely the risk that
document names.

**Deferred to Session 4 on 2026-09-03, with a condition.** Session 4 owns the family-wide rule and
Session 5+ opens every repository anyway, so fixing three pages now means three PRs and then three
more when the spec changes their shape. That is the argument `0003` § 7 already made about
back-navigation, and it holds here. The condition exists because this finding is *itself* a case of
a generalisation being written down and not applied — deferring it again on the same terms would be
the second occurrence of the failure it describes. So it is carried as a **bound checklist item of
the Session 4 spec**, with the three counts above as its acceptance test, rather than as prose that
a later reader has to notice.

**Session 4 checklist item.** Every `<table>` on every published page sits inside an
`overflow-x` box, asserted by a test in the repository that generates the page — not by a
measurement taken once. Acceptance: `pl-review-sense` 7/7, `it-job-radar` 1/1,
`mini-traceroute` 2/2, and the four already-fixed pages stay fixed.

## 7. The gap in the stack

One, and it is clear: **RAG and retrieval evaluation**. Everything else a reader would look for is
covered — an agent with an evaluation harness (P3), fine-tuning against baselines (P4), structured
extraction with error detection (P5), MLOps with a measured detector (P1), applied statistics (P2),
the full supervised cycle (A3), data engineering (A2), time-series discipline (A1).

That is exactly what A5 was meant to be and never became. The plan's own guidance from the earlier
design session still stands: scope any RAG work around **retrieval evaluation**, not around a chat
UI — the portfolio's consistent argument is that things are measured, and a chat UI measures
nothing.

## 8. What this makes true elsewhere

Consequences, for the sessions that own them. None of these is implemented here.

**Profile README** — must list `doc-extract` at all; *Start here* becomes one row per role rather
than one flagship; the ⭐ moves.

**Index README** — A5 row struck; A6 and A4 move to Level B; `doc-extract`'s status corrected from
`M2 of 7` to what the repository records; the "Pinned on profile" line reworked.

**Session 3 (descriptions)** — `doc-extract`'s four conflicting progress figures reduced to one, at
the source that generates the rest. `wroclaw-air-insights` and `it-job-radar` need a licence, which
is not a description but is found in the same pass.

**Session 4 (spec)** — the family B pages need a claim as `h1`, which is the single highest-value
presentation change identified: it converts three repo names into three findings. Table wrapping is
already established as a family-wide rule rather than a per-repo fix.

**Session 2 (extensions)** — the RAG gap; ~~`doc-extract`'s missing CI and~~ its zero topics;
`car-price-ml`'s reported language; and `apply-scout`'s security debt, which belongs in an
extension proposal rather than in a presentation pass, because naming it in the README is the
minimum and confining the loop is the real fix. *(The CI landed ahead of the session, 2026-09-03
— see §3.4.)*

**Ahead of all of them** — § 6.1, the contact details. It is a single edit to one README and it is
the only item in this review that changes what a convinced reader can *do*. *(Half done
2026-09-03: the account fields are set, the README edit is not — and it was always the half that
is a file. It is item 4 of the handoff in `0003` §9.)*

## 9. Open items

- ~~Whether the two Level B pages (`auth-log-scan`, `mini-traceroute`) get promoted into the
  profile README's demo table~~ — **done**, both are in it.
- Whether Level B survives as a tier at all once `token-budget` and `pl-review-sense` join it —
  it will then hold five items of three quite different kinds.
- ~~`infra-docker-workmate`, per § 5.~~ **Decided
  2026-09-03: unpinned from the portfolio, repository kept.** § 5 recorded the removal as declined
  and the drift as continuing; both are now settled without deleting anything. The contents were
  never portfolio-only — they live in `P0w3r223/infra-docker-workmate`, private, 1.17 MB, last
  pushed 2026-08-21, **200 commits ahead** of the pointer the index held. The index named it in
  `.gitmodules` and nowhere else; `README.md` never mentioned it. So only the submodule link goes.
- ~~**The git identity on `doc-extract`** (§ 6.3)~~ — **fixed at the cause**, not just in history.
- ~~Three findings from `0002`~~ — all three **fixed**: the index says 13.9 MB, no project is
  listed twice, and A6 is now B5 with its missing page stated rather than implied by an empty
  column.
- ~~**Provenance inside the published `it-job-radar` dataset.**~~ **Closed by `it-job-radar#23`.**
  `docs/data/snapshots.parquet` had a
  `git_sha` column recording which commit produced each of its 25 snapshots — **15 distinct
  hashes, every one dangling** after the rewrite. The page stamp had been repaired; this column had
  not, because rewriting it edits a published data artifact rather than a claim about one, and the
  manifest's contract covers the file. The consequence was sharper than the deferral sounded:
  `manifest.json` named snapshot 25 as `de4d944` while the parquet called the same event
  `ea6c199`, so the dataset disagreed with itself about one build.

  **Remapped.** All 15 paired by tree plus both dates against the pre-rewrite mirror, each landing
  on exactly one commit reachable from `origin/main`; the map is injective and reproduces
  `ea6c199 → de4d944`, which the page-stamp repair had reached independently by hand. Snapshot 1
  keeps its null — mapping every value would fabricate provenance for a row that has none. The
  page rebuilds byte-identical, so the `drift` job is the proof rather than a formality, and three
  new tests read `docs/data/` directly, which **no test in the suite did** — which is exactly how
  the dangling column survived a suite that otherwise builds a synthetic database for everything.
  Those tests carry three gaps of their own, and the artifact was written by an unsupported
  `pyarrow`; both are on the queue in `0003` §9.

  **Chosen 2026-09-03: remap.** "Recoverable from the backups" was checked rather than repeated —
  all 15 hashes resolve as commits in
  `_rewrite-backups-2026-09-02/…/it-job-radar.git`, so the pairing has a
  source. The alternative considered was dropping the `git_sha` column outright, on the grounds
  that `manifest.json` carries the file's contract. It was rejected on the portfolio's own
  argument: a defect in provenance is not answered by deleting the provenance. Method is the one
  already used for the four page stamps — pair by tree plus both dates, disambiguate by
  reachability.

- ~~**Contact details (§ 6.1) — decided 2026-09-03.**~~ **Filled the same day, except `name` and
  a typo in the bio — and except the README, which is not an account setting at all.** See § 6.1.
  `name`, `bio`, a public `email`, the URL
  field and *Available for hire* are being filled by the author; they are account settings, not
  files, and no token this project holds carries the `user` scope needed to write them. The URL
  field points at the `doc-extract` live site rather than at the profile, because the profile
  README already *is* the portfolio index on that same page — so the one link in the sidebar
  should be the thing a README cannot be, a live artifact one click away. If a single landing
  page for the portfolio is ever built, that link moves there.
