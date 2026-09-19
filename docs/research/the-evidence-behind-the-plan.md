# What the evidence says a portfolio is worth, and what this one still needs

Date: 2026-09-18
Status: accepted
Author: Piotr Cząstkiewicz
Related to: [`0010`](../audit/0010_the-portfolio-audit.md) (the portfolio audit),
[`0009`](../audit/0009_the-review-of-the-whole-system.md) §7 row 11 (the profile README),
[`ADR-0004`](../adr/0004_what-carries-the-page-spec.md) (what carries the page spec)

---

## 1. What this is, and what it replaces

Eight research passes — four perspectives run twice — against one question: what does a
recruiter-facing portfolio have to be, and how far is this one from it. Plus an inventory of
what is actually on GitHub today, taken from the API and from the trees rather than from
memory.

**This document replaces three planning documents, which are deleted with the commit that adds
it.** They were `plan-portfolio-github.pdf` (stage 1, ~20 weeks, projects A1–A5 and B1–B3),
`plan-portfolio-etap2.pdf` (stage 2, ~19 weeks, projects P1–P5) and
`portfolio-polish-backlog.md` (the recruiter-facing redesign backlog of 2026-07-27, marked
*executed 2026-07-28*). None was tracked by git — they lived in the directory above both
repositories — so §5 below records what they asked for and what became of each item. **Nothing
in them is lost except the file.**

**What this document is not.** It is not a measurement of this portfolio's conformance — that
is `0010`'s job and the checker's. It is not a new programme either: §7 says how it folds into
the one `0010` §3.1 already runs.

**A standing caution about the field itself.** Three of the four research perspectives
independently reported the same thing: the figures everyone quotes about recruiters — *87% of
recruiters check GitHub*, *6 seconds on a CV*, *open-source contributors are 38% more likely to
land interviews* — have no primary source. One of them is attributed to a Stack Overflow survey
that contains no such question. They are content marketing, they are repeated by every guide,
and **none of them is used below**. Where a number appears here it has a named source, and
where the evidence is an opinion it is called one.

## 2. The five findings the plan rests on

### 2.1 The first filter is a coin flip, so the portfolio does not work there

Recruiters predicting who will pass a technical interview from a CV are right **55%** of the
time (76 technical recruiters, ~2 200 judgements over 1 000+ CVs whose owners had measured
interview outcomes); a second study puts it at **53%**, with inter-rater agreement of
Fleiss' κ = 0.13 — and hiring managers scored **worst of all groups at 48%**. The strongest
single predictor of an offer was the count of typos and grammatical errors; the strongest
predictor of rejection was the absence of a brand-name employer.

The corroborating fact is sharper than the studies: interviewing.io built a production model
on ~200 000 technical interviews that beats both recruiters and LLMs, and **its features are
LinkedIn trajectory — titles, transitions, how work is described, profile completeness.
Portfolio, GitHub and side projects are not among them.** A company with a decade of outcome
data, building a commercial tool, did not find the portfolio worth including.

*This is the load-bearing finding of the whole document*, because it relocates where the
portfolio pays: not in screening, but in the interview round where somebody asks about it.

### 2.2 In that round, the evaluation harness is the signal

The question interviewers ask, quoted verbatim from a corpus of 51 hiring processes:
*"Is there an actual eval framework here, or is it vibes-based?"* — described in the same
source as *"the single highest-signal question on the list"*. Second is the per-query cost and
latency argument, which one source calls what separates *"production thinkers from
prototypers"*. Third is monitoring after deployment.

The 2025–2026 red flag is the mirror of it: **a candidate who cannot explain their own code.**
71% of engineering leaders (n = 400) say AI has made technical skill harder to assess, and
on-site rounds rose from 24% (2022) to 38% (2025) in response.

The peer-reviewed framing that organises all of this is from 2013 and still unrefuted: activity
traces are read as **more reliable than a CV's claims**, but only the traces that are *cheap to
verify and expensive to fake*. Stars and badges are cheap to fake, so they carry nothing. A
measured result with the command that produced it beside it is expensive to fake, so it does.

### 2.3 The channel beats the artefact

How Polish IT professionals found their current employer (Bulldogjob community survey 2025,
4 331 respondents after quality screening): **job boards 38.2%** (general 19.7% + specialist
18.5%), **friends 27.0%**, **recruiter outreach 14.5%**, social media 10.8%, employer's own
site 4.2%, conference 2.3%.

The demand side (No Fluff Jobs, *Rynek pracy IT w Polsce 2025/2026*, offers published on
nofluffjobs.com through 2025, +44% year on year), read from the report rather than from
summaries of it:

| | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| junior share of postings | 8% | 5.9% | **5.3%** |
| senior share | 43.7% | 55.5% | **59.7%** |
| applications per posting, whole market | 40 | 44 | **24** |
| applications per posting, **AI** | — | 36 | **16** |

Applications per posting by work mode: **remote 39, on-site 16, hybrid 13** — remote draws
*"2.5× more applicants than on-site and 3× more than hybrid"*. Category shares: Backend 20.1%,
**Data & BI 12.4%**, Fullstack 10.5%, DevOps 7.8%, **AI 3.9%**. The report's own comment on the
last one: *"O sztucznej inteligencji wciąż więcej się mówi niż jest to faktycznie rosnąca
kategoria"*. Top requirement across the whole market: **Python, 23.1% of postings**.

Just Join IT's independent count agrees where it matters — junior **4.79%** — and disagrees
where the definitions differ (remote 67% by *option to work remotely* versus NFJ's 42.8% by
*declared mode*). **Do not quote one remote figure**; the honest range is 43–67% with the
definition attached. The junior share is the number that survives both taxonomies.

*Read together:* the AI category is narrow and the least crowded on the market, remote is the
most crowded channel there is, and the portfolio is not a channel at all — it is what waits at
the end of one.

### 2.4 The ornamental layer is measured and worthless

- **Stars**: ~6 million suspected fake stars found in GitHub metadata 2019–2024, with AI/LLM
  projects among the main targets; the promotional effect lasts under two months and then
  damages the repository's standing (ICSE'26).
- **Achievement badges**: peer-reviewed study of >6 000 developers — badges are *"generally
  poorly correlated with developers' qualities and dispositions"*, and a growing number of
  users deliberately hide them.
- **Profile stat widgets**: `github-readme-stats` (79.8k stars, the most common one) opens its
  own README with *"This repository is no longer maintained"* and warns that its public
  instance *"can be unreliable due to rate limits and traffic spikes"* — i.e. it renders as a
  broken image exactly when somebody is looking.
- **The contribution graph**: trivially shaped by a private-contributions toggle, so it carries
  no information either way.

And the finding that matters more than those three, because it points at something to *do*
rather than avoid: 4 226 README sections across 393 repositories were hand-coded, and *"many
README files lack information regarding the purpose and status of a repository"* while **what**
and **how** are near-universal. A second study (1 950 READMEs, 10 languages) found that
*how-to-run* sections **do not differentiate at all** — everyone has them. **So the cheapest
unoccupied differentiator is one sentence of *why this exists* and *whether it is maintained*.**

### 2.5 A hosted demo has no measured advantage, and the ground moved under it

No study, no A/B test and no hiring-manager account was found comparing an interactive demo
against a static page carrying measured results. The only survey with a counterfactual question
(60+ hiring managers, 2021, frontend): 65% would look at a portfolio site, and **51% said a
candidate without one would not have lower chances**. One respondent: *"Better to have no
portfolio website than one that looks bad or is broken."*

Meanwhile the free tier moved. Since **2026-07-08** — dated from forum reports, because
**Hugging Face's own Spaces changelog carries no entry for it** — Gradio and Docker Spaces
require a paid plan; static Spaces stay free; a free personal account in good standing may host
**2 Gradio Spaces on ZeroGPU**, which is Gradio-only. The trap for a portfolio is in the quota
table: an **unauthenticated visitor gets 2 minutes of GPU per day at the lowest queue
priority** — that is the recruiter. Streamlit Community Cloud sleeps after 12 hours of no
traffic; Render's free tier sleeps after 15 minutes and takes about a minute to wake.

GitHub Pages, by contrast: 1 GB site, 100 GB/month soft bandwidth limit, no sleep, no cold
start, no cost. **The twelve static pages are the correct decision on the evidence**, and the
argument for adding a hosted demo is a guide-book claim with platform economics against it.

### 2.6 Two findings specific to a Polish candidate

**The automated sieve labels this profile junior by default.** GPT-4 was given eight GitHub
profiles and asked to staff a six-person team, over 3 657 profiles from the US, India, Nigeria
and Poland (216 Polish), 2 400 runs. The model saw **only login, bio and location** — not
repositories, not READMEs, not stars. A profile located in **Poland was assigned the role
"Junior developer" 76% of the time**, the highest of any region, and "Data scientist" **12%**
against **42%** for the US. Swapping the location from PL to US raised the candidate's
recruitment probability from 64% to 70% (p < 0.05).

The actionable half is not the bias — it is that **the profile bio is a separate communication
surface and it is read by the sieve.** ~~And ours is empty: writing *AI Engineer · LLM
evaluation · MLOps* into it costs a minute and is cheaper than any project.~~ **The bio has been
filled since 2026-09-03 and this document measured it wrong**; §9 is the correction.

What the re-measurement found instead is sharper, because it is about this same paragraph's
premise. **The sieve reads three fields and this profile supplies two.** `location` is empty,
and every figure above is stated of *a profile that states a location* — the 76% and the 12%
of a Poland-located one, the 42% and the 70% of a US-located one. The study varied that field;
it never emptied it. Whether an absent location reads to the model as Poland, as nothing, or as
some default is **not something this research measured**, so §8's rule applies and no direction
is claimed.

**An AI assistant in a project's history is not a flag here — the verification layer is the
differentiator.** 87% of Polish developers use AI daily (AWS *DevHorizon Poland 2026*, n = 500),
against 51% globally; 78% say the engineer's role is moving toward *"koordynacji, orkiestracji
i nadzoru cyfrowych asystentów"*; 77% name critical evaluation of what the AI produced as the
hardest and most important future competence. Against that, 66% of developers worldwide report
*"AI solutions that are almost right, but not quite"* and 46% actively distrust the output.

So the thing that distinguishes a portfolio built with an assistant is **visible verification**
— which is precisely the evaluation harness, the error detection in the extraction project and
the promotion gates in the MLOps layer. That is an argument to make out loud in an interview,
not a liability to hide. The risk it neutralises has a name from a peer-reviewed focus study of
18 recruiters: *"Practice of Presenting Unauthentic Work"*, described by one participant as
*"a grave breach of professionalism"*. Disclosure with a factual account of the process is a
**defensive** move of known value; nobody has measured an offensive one.

### 2.7 Where the market is going, and one claim that does not survive a second measurement

Rising, confirmed by two independent datasets: **agents** (Lightcast: agentic-AI cluster 0.06%
→ 0.23% of US postings, +280%; Dice, 7 million postings: AI Agents +503%), **RAG** (+275%),
**prompt engineering as a skill** (+253%, while the *job title* "Prompt Engineer" collapses),
and — the one that matters most here — **deployment and integration**: AI Infrastructure +366%,
Enterprise Integration +638%, Observability +251%.

**The claim that fine-tuning demand is falling did not survive.** A first pass reported it from
a single author's dataset. A second measurement found no dataset publishing a decline for it in
either direction, and found the *deployment* half of the same claim contradicted outright —
deployment skills are among the fastest-growing categories in both corpora. So: *"integrator"*
is confirmed, *"instead of trainer"* is unproven, and this document does not assert it.

For the Data Scientist track the picture is different and worth stating plainly: a Polish DS
posting asks for **classical ML, Python, SQL and visualisation** as must-haves, with LLM/GenAI
listed as a *bonus*. And Polish "Data" is overwhelmingly data engineering — Spark, Databricks,
Airflow, Snowflake — at 10.8–12.4% of all postings, against AI's 3.9%. Cloud in Poland is
**Azure and GCP**, not AWS.

## 3. What is on GitHub today

Taken 2026-09-18 from the GitHub API, the published pages and the working trees.

**The twelve repositories.** All public, all MIT, all with a description and topics (6–18
each), **CI green on `main` in all twelve**, eleven with a GitHub Pages site and a homepage set
(`token-budget` has neither, by design). Stars 0–1 — the portfolio has no external social
signal, which §2.4 says is the correct amount to care about.

**The eleven published pages all answer `200`, and each opens with a measured claim** rather
than a description — *"A 13.9 MB model prices this market better than a 590 MB one"*,
*"Most junior IT offers in Poland are not development jobs"*, *"HerBERT reaches 0.986 against
the baseline's 0.944"*. This is §2.2's "expensive to fake" property, and it is the part of the
portfolio that is already right.

**The profile README** exists, 63 lines, with positioning, a "Start here" line for each of the
two roles, a table of five flagship projects, a table of eleven live demos, a stack block and a
link to this index.

**Six pins**: `doc-extract`, `ab-lab`, `apply-scout`, `mlops-car-price`, `wroclaw-air-insights`,
`it-job-radar`.

**What the inventory found missing**, each measured rather than assumed:

| | measured |
|---|---|
| custom social-preview image | **0 of 14 repositories** — every link pasted into LinkedIn or an ATS renders as GitHub's grey default card |
| ~~profile bio~~ | ~~**empty** — the one field §2.6's sieve reads~~ **Wrong, and corrected in §9.** Filled since 2026-09-03, 129 characters, closed as a finding in `0004` §6.1 |
| profile `location` | **empty** — the *third* field §2.6's sieve reads, after `login` and `bio`, and the one that document's figures are conditioned on. Found by the re-measurement that overturned the row above |
| profile `name` | the bare handle `P0w3r223` — `0003` §9 and `0004` §6.1 both record it set to the legal name on 2026-09-03, so **the field moved back**. §9 has the likely reason, stated as likely. The sieve does not read this field |
| `roadmap`-labelled issues | **2 of 12** repositories have any open (`apply-scout` 5, `mlops-car-price` 7) |
| animated demo | **1 of 12** (`apply-scout`) |
| README against the stage-2 definition of done | by section headings, only `apply-scout` carries all seven; `car-price-ml` is missing five, `wroclaw-air-insights` and `pl-review-sense` four each |
| decision records | 0 in `wroclaw-air-insights`, `auth-log-scan`, `mini-traceroute`, `token-budget`; 12 in `apply-scout`, 11 in `ab-lab` |

*The README figure is a heading heuristic, not a verdict* — a README can answer a question
without a heading naming it. It is reported as a direction, and §6 acts on the five flagships
rather than on all twelve for that reason.

**The audit's own state**, from `python -m tools.queue`: 15 sessions in `0010` §3.1, **6 with a
row**, 9 to go; **8 items open, 14 closed, 10 deferred**.

## 4. Where this portfolio stands against its peers

The peer tier is measurable because DataTalks.Club publishes graded capstones with links:
**157 submissions** in LLM Zoomcamp 2025 and **230** in MLOps Zoomcamp 2025, each peer-reviewed
against a published rubric. The best of them carry MLflow with registry-alias promotion,
Evidently drift, Terraform, integration tests — and **9 stars**. The best LLM one carries a live
demo, screenshots, measured hit rate, 9 tests, CI, a limitations section — and **0 stars**.

Two things follow. **Stars are not the currency at this tier** — the editorially celebrated
portfolios sit at 8–1 407 stars and most are notebook collections last touched years ago. And
**measured results on a page are rarer than a demo**: among the exemplars reviewed, a working
demo was common and a page carrying reproducible numbers was close to absent.

The single most useful sentence found in the whole research came from a hiring manager
describing his own company: *"maybe 1 candidate in 10 has any sort of portfolio of projects to
share. And of those candidates who do have something to share, the quality is overwhelmingly
poor."* — and, in the same comment, *"we have passed on candidates because of them"*. The
portfolio is therefore **a rarity differentiator and a negative filter**, not a cause of hiring.

**Nothing in the research criticised a junior portfolio for being over-engineered.** Every
recurring criticism ran the other way: same datasets, tutorial steps, a metric instead of a
decision, no business conclusion. That is the direction of the risk here, and it is not the
direction this portfolio errs in.

## 5. The three plans this document replaces, and what became of them

Recorded so that deleting the files loses nothing.

**Stage 1 (`plan-portfolio-github.pdf`, ~20 weeks).** Level A: A1 `wroclaw-air-insights`,
A2 `it-job-radar`, A3 `car-price-ml`, A4 `pl-review-sense`, **A5 `studia-rag` — the intended
flagship, a RAG assistant over course materials with an evaluation set of 30–50 questions**.
Level B: B1 `mini-traceroute`, B2 `auth-log-scan`, B3 the car-price front end. Profile
fundamentals in week 1; CV updated twice.

*What happened:* **A1–A4 and B1–B3 all exist and are live. A5 was never built** — the profile
carries `token-budget` in its place, which the plan never named. The RAG gap in §2.7's
frequency table is the direct consequence, and §6 item 9 is what this document does about it.

**Stage 2 (`plan-portfolio-etap2.pdf`, ~19 weeks).** P1 `mlops-car-price`, P2 `ab-lab`,
P3 `apply-scout` (flagship), P4 `pl-jobs-lora`, P5 `doc-extract` — **all five exist and are
live**. The stage also specified a per-project definition of done (problem → demo →
architecture → results → run in three commands → decisions → limitations), a five-section
`CLAUDE.md` in every repository, `roadmap` issues as a public plan, and a rhythm of one branch
and one pull request per session with a decision record for each significant choice.

*What happened:* the engineering half was executed and then some — the page specification in
`0007` §5 and the checker that enforces it did not exist in either plan. **The presentation and
distribution half was not**: technical write-ups after P1/P3/P4 with links from the profile and
LinkedIn (zero), open-source contributions of 2–4 pull requests from week 7 (zero), the
20-minute interview simulation after each project (no trace), applying in parallel from week 6
rather than after everything (not started), and `roadmap` issues in every repository (2 of 12).

**The backlog (`portfolio-polish-backlog.md`, 2026-07-27, marked executed the next day).**
It found `apply-scout` private, no profile repository, inconsistent descriptions and no topics,
and a stale pin target. *What happened:* all of those are closed — `apply-scout` is public, the
profile repository exists, descriptions and topics are set everywhere, six real pins. Its
remaining items were the demo GIF and the profile pins; the pins are done and **the GIF is
still 1 of 12**.

## 6. What to do, in the order the evidence supports

The rule applied to every item: **it must follow from §2, it must not add to the repositories
anything they do not themselves verify, and it must not touch the checker, the guards or
`0007`.** Everything below is metadata, one sentence, or lives outside the repositories.

### Tier 1 — hours of work, highest leverage, and a scan session will never produce it

1. **A 1280×640 social preview for all twelve, topics filled toward the 20 allowed, and a
   profile `location`.** ~~…and a profile bio.~~ The preview is the only surface that renders
   *outside* GitHub — in a LinkedIn card, in a message, in an ATS — and 0 of 14 have one.
   ~~The bio is the field §2.6's automated sieve reads, and it is empty.~~ **The bio half of
   this item was already done before the item was written** — §9. What replaces it is the field
   beside it: **`location` is empty**, it is the third of the three §2.6's sieve reads after
   `login` and `bio`, and it is the one that document's figures are conditioned on. It is also
   the owner's to set and nobody else's, for the same reason the bio was — no `user` scope;
   `0008` §5 records the boundary, though its row names `name`, `bio`, `email`, `blog`,
   `hireable` and social accounts and **not** `location`.
2. **One sentence of *why this exists* and *whether it is maintained* at the top of every
   README.** §2.4: it is the documented systemic gap, and it is one line per repository.
3. **A defence document for the three flagships, kept privately and not committed.** Per
   project: the evaluation set and how it was labelled, the baseline, which cases still fail,
   what changed after the evaluation, the per-query cost, the failure modes, and the answer
   shaped as *"I chose X over Y because Z; the downside was A; I accepted it because B; if it
   grew I would change C"*. **This is the highest-return item in the document**, because §2.1
   says the entire value of the portfolio is realised in the round where somebody asks — and
   stage 2's plan called it a hard rule and left no trace of it.
4. **Make the profile README a hierarchy rather than a list.** Three "Start here" lines —
   **AI Engineer → `apply-scout`** (the agent and its harness, §2.2's signal),
   **Data Scientist → `ab-lab`**, **Data Engineer → `it-job-radar`** — and the rest as an index
   below. Two independent Polish sources say the same thing about finished projects: *"Portfolio
   musi być skończone"* (1–3 of them) and *"Jeden dobrze zrobiony projekt jest lepszy niż
   dziesięć niedokończonych"*. **Adding the third track is a finding, not a preference**: Polish
   "Data" is 10.8–12.4% of postings against AI's 3.9%, and the two data-engineering projects are
   currently the least represented thing in the positioning.

   **Executed 2026-09-18** in `P0w3r223/P0w3r223`. `apply-scout` took the AI Engineer line,
   `it-job-radar` the new Data Engineer one, the two overlapping tables became one index, and
   every project line now quotes its own page's opening claim — ten of eleven byte-exact against
   the checker's parser, the two exceptions declared in the file.

   **And one residual, recorded as a decision rather than left as an omission.** The Data
   Engineer track **rests visibly on one project**. §2.7 describes Polish "Data" as
   *"overwhelmingly data engineering — Spark, Databricks, Airflow, Snowflake"*, and the stack
   block offers ETL pipelines, DuckDB / Parquet, SQLite and data contracts — all of which the
   repositories genuinely carry, and **none of which is one of those four**. The second data
   project, `wroclaw-air-insights`, reads in the index as forecasting rather than as a pipeline.
   So the track is honest and defensible on `it-job-radar` alone, and it will not match the
   keyword filter it was added in response to. Closing that gap is a Tier 3 decision about what
   to build, not a Tier 1 edit — it belongs beside item 10's cloud question, and it is written
   down here so the next reader meets it as a known cost of the track rather than as a gap
   nobody noticed.

### Tier 2

5. **A `results` and a `limitations` section in the five flagships** — not in all twelve. §4:
   every recurring criticism of peer portfolios is *too shallow*, never *too engineered*.
6. **An animated demo for `doc-extract` and for `car-price-ml`'s form**, where interaction is
   the point. For a project whose output is a table, a GIF adds nothing the page does not
   already say — and the one measured study found GIFs' association with popularity *negligible*.
7. **Stop the roadmaps pretending.** Close what is done, keep issues only where the work is
   real. `ab-lab`'s four were all done and all open until this week, which is the shape `0010`
   A-6's D axis raised against the repository's own front page.
8. **Shorten this repository's public map.** Its cells run 80–100 words per project — accurate,
   and unreadable in the minute §2.1's evidence allows. The thesis belongs here; the detail
   belongs on the page.

### Tier 3 — decisions rather than tasks

9. **The RAG gap.** It is the largest single gap against the postings (39.8% of them; 40%+ of
   take-home assignments) and it is what A5 was going to be. But the most-cited mistake in the
   same literature is **choosing the technology before the problem** — *"I want to build a RAG
   app"* with no named user. So: first **show the retrieval that already exists** — `apply-scout`
   measures its own retriever — and build a RAG project only with a named user, ideally with
   `ab-lab` as the apparatus that chooses between variants under power and multiple-comparison
   control. One artefact would then serve both career tracks.
10. **Cloud (Azure/GCP for Poland) is absent.** The evidence for cloud as a *portfolio* signal is
    much weaker than for evaluation, so this is low weight: one project if any, never four.
11. **No hosted demo.** §2.5. This is a decision made on evidence, and it saves both money and
    the risk of a recruiter meeting a sleep screen.
12. **Channel, which outranks everything above.** §2.3: hybrid roles in Poland draw a third of
    the applicants remote ones do, and stage 2's own rule — *apply in parallel, not after
    everything* — was never started. Aplikowanie now outweighs the seventh scan session.

## 7. What must not change, and how this folds into the audit

**Unchanged**, because the evidence supports each and the alternative is documented as worse:
measured results on static pages; decision records; CI; a single badge; twelve separate
repositories rather than a monorepo (twelve verifiable activity traces instead of one); and the
audit that holds the pages to a written specification.

**Two sequencing corrections, not a new programme.** Tier 1 goes **before** scan sessions 7–12,
because those sessions verify what exists and will never produce a social preview or an account
field, and because it costs hours. And the profile README, the account fields and the social
previews belong on the list of surfaces the audit covers — which is `0009` §7 row 11, already
being answered elsewhere, so this widens that row's scope rather than opening a new one.

**§9 is the argument for that second half, not an illustration of it.** Three account fields
were re-read hours after this document was accepted — two of the three §2.6's sieve reads
(`bio` and `location`; the third is `login`, which cannot move) plus `name`, which the sieve
does not read at all — and they came back in three different states: one **measured wrong
here** (`bio`), one **never covered by anything** (`location`), and one **standing against a
finding two audit documents record as closed** (`name`). No instrument in this repository reads
any of them, so none of those three states could announce itself; each had to be found by a
person deciding to look. That is what putting them on the audit's list of surfaces would
change, and it is why the widening is the point rather than the footnote.

## 8. What this research could not establish

Stated so a later reader does not mistake absence for a finding.

- **No controlled evidence that a portfolio changes callback rates exists.** No correspondence
  study, no audit study, no platform A/B test manipulates a portfolio artefact. What exists is:
  employers say they look; practitioners split roughly in half; and the one production model
  trained on outcomes does not use it. Anyone claiming otherwise should be asked for a DOI.
- **No Polish source counts skill frequencies in AI/DS postings.** The closest candidate is a
  2026 paper from Wrocław University of Economics, behind a paywall. This is a gap that
  `it-job-radar` could close by measuring it — which would be an exhibit as well as an answer.
- **No documented case of a candidate disclosing an AI-assisted portfolio**, positively or
  negatively. The risk shape is documented; the reward is not.
- **No Polish hiring manager on record about interviewing for AI Engineer specifically.** The
  four Polish accounts found are about general IT or analytics, and the most detailed one about
  GitHub is from 2021.
- **Reddit and 4programmers.net were unreachable** to the research tooling in both passes
  (user-agent block and 403 respectively, with no Wayback snapshots for the latter). The
  anonymous Polish practitioner voice is absent from this document, and closing that gap needs
  a person with a browser.
- **Whether GitHub's automated readers treat an absent `location` as Poland, as nothing, or as
  something else.** Added 2026-09-18 with §9. The source study set the field to one of four
  regions and swapped it between two; it **never left it empty**, so the paper cannot answer
  this and neither can this document.

## 9. Errata, 2026-09-18 — the inventory row that was wrong, and the two fields beside it

Raised hours after this document was accepted, at the start of the session that was to execute
§6 Tier 1. **The whole of §6 Tier 1 item 1 was to be done first, so its three sub-items were
re-read from the API before being acted on** — which is the only reason the row was caught at
all. A reader who had trusted §3 would have spent the minute §2.6 costs writing a field that
already said something.

### The correction

**§3's table said the profile bio is empty. It is not, and it has not been since 2026-09-03.**
`gh api users/P0w3r223 --jq '.bio | length'` returns **129**. Two audit documents record the
field being filled and the finding closed on that date — `0004` §6.1 (*"~~`bio` null~~ —
**set**; its wording is the author's and settled"*) and `0003` §9, the reconciliation that
closed it, which quotes *"Open to AI/ ML engineer"* and, a hundred lines further down the same
section, names **the bio's stray space**. The live field today ends in that text, with that
space. *`0003` presents the quote as what the field said rather than as a fragment of it, so
calling it a closing clause would presuppose the reading the next subsection declines to
choose; what is measurable is that the live field ends with it.*

Corrected at **five** sentences in four places — §2.6's actionable half, §3's table row, §6
Tier 1 item 1, and two in §7 that argued from the bio being empty — because
`docs/reference/failure-classes.md` `ST-3` is a correction applied in some places and left
standing in another, and `0010` §5 records instances of it without a count, deliberately, for
the same staleness reason this errata exists. *The first draft of this paragraph said "three
sites", which was a hand count of a sweep whose whole purpose is to prove the sweep was
complete — wrong in the direction of under-reporting, and caught by review.*

### What cannot be established, and is therefore not asserted

**Whether the bio's opening sentence is older than this document.** The owner's recollection is
that they wrote the bio after reading the research; the record shows the field filled fifteen
days earlier, and the live text ends in a clause `0003` quotes. Both can be true — the field may
have been **extended** on 2026-09-18 and `0003`'s clause kept. **GitHub publishes no history for
a profile field**, so no command settles it and this document does not choose. What the
disagreement does settle is the only thing §3 needed: the field was **not empty**, so the row
was wrong when it was written and not merely overtaken.

*Recorded rather than resolved in the owner's favour, and recorded rather than resolved against
them.* `0010` §5 has the shape from the other direction — a true measurement with a false
sentence around it. This is a sentence that has two readings and one measurement, and the
measurement only reaches as far as one of them.

### The two fields the re-reading found beside it

Neither was in §3, and for two different reasons. `location` is one of the three §2.6 names and
§3 measured only the bio of them. `name` is not one of the three at all — the sieve does not
read it — and it surfaced because the same command returned it, which is the whole character of
this finding: nothing was looking for either.

- **`name` reads `P0w3r223` — the bare handle.** `0004` §6.1 and `0003` §9 both record it set
  to the legal name on 2026-09-03, and `0004` names the bare handle as *"the specific complaint
  above"* that setting it answered. The most likely explanation is deliberate and is not a
  regression, and the finding it answers to is **`0011` §4's R-5** — *"the public handle bound
  explicitly to the legal name"*, `in main: yes`, graded `PII, almost certainly deliberate`.
  **Not R-1**, which this paragraph named in its first draft: R-1 is author and committer
  metadata living in 26 `refs/pull` refs of the archive, is not in `main`, and is unreachable
  by a clone — so unsetting a profile field mitigates nothing about it. *A mechanism that
  cannot produce the effect, offered in the paragraph that congratulates itself on refusing to
  state inference as fact.* **And nothing in the record says R-5 is why** — no §, no errata,
  no brief — so the reason stays stated as likely: a closed finding that has quietly come
  undone reads identically to one that was undone on purpose.
- **`location` is empty, and §2.6 is conditioned on it.** The study §2.6 rests on showed its
  model *login, bio and location* and nothing else; every figure quoted there is stated of **a
  profile that states a location** — the 76% and the 12% of a Poland-located one, the 42% and
  the 70% of a US-located one. This profile states none, so the paragraph's own premise is unmet
  on the surface it is about. §8 now carries what that means as an open question rather than a
  direction.

### What it costs, and who can act

All three fields are the owner's alone: `gh auth status` reports the token's scopes and **no
`user` scope is among them**, which is the standing boundary `0008` §5 records for the profile
fields — though that row names `name`, `bio`, `email`, `blog`, `hireable` and social accounts,
and **not `location`**, which sharpens this section's *never covered by anything* rather than
softening it. *The scope list is a reading from a command run in this session, not a figure any
document carries; the first draft attributed it to `0008` §6, which is the assumptions table and
carries neither the list nor the boundary.*

So this errata changes no field. It changes what §6 Tier 1 item 1 asks the owner for —
`location`, not the bio — and it adds the three fields to what `0009` §7 row 11 should cover,
which §7 above now argues directly.

### What this errata does not bound

§3 opens *"Taken 2026-09-18 from the GitHub API, the published pages and the working trees"*,
and that sentence vouches for every row in its table, including the one now known to be wrong.
**This errata does not establish how a same-day API read returned an empty bio**, and therefore
cannot say whether the defect was one row misread or an account-half pass that did not run as
described. The rest of the table was re-read here and holds — six pins in the agreed set,
stars 0–1, twelve MIT licences, eleven pages with a homepage set, `token-budget` with neither,
`hireable` true, and 0 of 14 social previews — but *held on re-reading* is a different
statement from *was measured correctly the first time*, and only the first is claimed.

*One asymmetry worth recording, because the first draft of this paragraph got it backwards.*
The social preview can be **read** from the API — GraphQL's `usesCustomOpenGraphImage`, which is
what re-measured it here — and cannot be **written** through one, REST or GraphQL; it is a web
form. So §3's hardest-looking row is the one the API answers cleanly, and the field that turned
out wrong is one of the easy ones. Which is the argument for the widening, not against it: the
difficulty of reading a field predicts nothing about whether anybody read it.

### What is waiting for the owner, and where it is — read 2026-09-18, after that day's merges

Three things, and **no session can do any of them**. The reason is one for the first two and a
different one for the third, and both are already established above: `gh auth status` reports
`delete_repo`, `gist`, `read:org`, `repo` and `workflow` and **no `user` scope**, so the profile
fields are read-only to every instrument here; and the social preview is readable through GraphQL
and writable only through a web form.

1. **`location` — still empty.** Re-read from the API after `c75b2b8`, `b5106dc`, `766203a` and
   `e9e2c22` landed: the field is `null`. Nothing in this repository has moved it, nothing can,
   and every figure §2.6 states is conditioned on a profile that states one.

2. **The bio is filled, and is now narrower than the README beside it.** The correction above
   established that the field is not empty. What the same re-reading did not ask is whether it
   *agrees* with the profile README, and it does not. The README opens on three tracks, AI
   Engineer · Data Scientist · Data Engineer; the bio names **one** of them, closing on *Open to
   AI/ ML engineer* — where `ML Engineer` is the separate junior role the README lists fourth,
   not `Data Scientist` and not `Data Engineer`, and the pair carries a stray space.
   **`c75b2b8` widened this gap rather than opening it**: the README read *AI Engineer / Data
   Scientist* before it, and the bio did not name the second of those either. *The first draft
   of this paragraph said the bio named two of the three and dated the disagreement to that
   commit — both wrong to one `gh api users/P0w3r223 --jq .bio`, in the subsection whose whole
   subject is a claim about this field that a one-command re-read refutes.* **The bio is the
   field §2.6's sieve reads and the README is not**, so the narrower of the two is the one
   doing the work, and the wider one
   is invisible to the filter it was written for. The field holds 129 characters against a limit
   of 160, so carrying all three costs a sentence and no project.

3. **Thirteen 1280×640 cards exist, and none is uploaded.** Rendered 2026-09-18, headlines read
   off the published pages by the checker's own parser. **Thirteen against this document's
   denominator of fourteen**, and the missing one is the profile repository — which is also the
   surface `0009` §7 row 11 has held open since before publication, so the gap is the same gap
   and not a new one. They live **outside every repository in this portfolio**, beside it, with
   their generator, a README and the record of the topic decisions; the path is deliberate and
   this document does not reproduce their contents. Uploading is one web form per repository —
   thirteen manual actions, verifiable afterwards by `usesCustomOpenGraphImage` and by nothing
   before.

**Why this list is here and not in `0010` §4.** None of the three is a finding against a
repository: no row owns them, no scan produced them, and no repair session can close them —
`0010` §3.1's sessions verify what exists. They are the residual of §6 Tier 1 item 1, which is
where the work was scheduled and where a reader will look for it. *And the reason a residual
needs writing down at all is that one named only in a session transcript is a residual nobody
inherits* — which is the same argument §5 makes about the three plans this document replaced.
