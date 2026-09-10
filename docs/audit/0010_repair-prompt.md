# Portfolio audit — REPAIR session                                      (prompt v2.0)

Paste this at the start of a repair session. It is the authority to act;
[`0010_the-portfolio-audit.md`](0010_the-portfolio-audit.md) is what to act on.

---

Close open rows in `0010` §4. The findings were made by scan sessions; you act on them.

Read §3.5 (the threshold), §3.6 (the mutation battery), §3.3 (per-repository commands), and
the rows you are closing. If §6 records a correction binding v2.0 or later, §6 wins over
this prompt.

## What you read, and what you deliberately do not

You read the row, and the code you are about to change.

You do **not** re-read the raw material the row was derived from — issue bodies, scraped
datasets, extraction corpora, committed prediction files. A scan session already judged
those and reduced them to a row. That reduction is the point: this session can push, open
pull requests, close issues and edit published pages, and it reaches none of the content a
scan session had to ingest to write the row.

If a row is too thin to act on without going back to that raw material, it is not ready.
Send it back to a scan session rather than reading around it.

## Selecting rows

Take rows that repair together — one repository, one pull request, one stage. §3.5 decides
what fits in a pass. A row marked `credential`, `personal data`, or any history rewrite needs
the owner's explicit go-ahead before anything is pushed, because it is outward-facing and
irreversible. `0010` R-1 is such a row and is open by design.

Rows blocked on a decision go to `architect` first, not into a commit.

## Working

- Branch, Conventional Commits, and a pull request body that says **why**. One stage per
  pull request. No Claude co-author trailer.
- Where the repository has a surface, its §3.3 page command runs before and after and is no
  worse after. `wroclaw-air-insights` needs `--fetch`, or the run reads nothing and exits 0,
  which looks identical to a pass. `car-price-ml` needs two runs, and generates
  `docs/app/styles.css` and `docs/index.html` from `src/car_price_ml/site/assets/` — edit the
  source and rebuild, or `test_the_committed_form_assets_match_the_source` fails.
- A new guard is proven by §3.6's three observations: collected and green unmutated, red on
  that guard's own assertion, green again after reverting. A skip is a pass, and `pytest -k`
  with a broken expression exits 5, which reads as red.
- `code-reviewer` over the diff before the pull request is proposed. Here it has something to
  review, which is why the step lives in this prompt and not in the scan prompt.
- Editing page text means the clause the checker names, not the sentence you would prefer.
  `0007` §5 binds the wording; a shorter headline that drops a figure breaks a gated clause.

## Closing

1. Mark each row closed in §4, citing the commit **on `main`** — this repository
   squash-merges, so a branch SHA exists for no later reader.
2. A row you decided not to repair stays open with the reason. Closing a row you did not act
   on is how the ledger stops being true.
3. Pattern rather than incident → §5. Contradicted this prompt → §6, version `v2.0`.
4. Session brief to `.claude/sessions/<YYYY-MM-DD>.md`.

## Standing rules

- Figures come from an instrument, never a hand count.
- Stdlib, `git`, `gh`, `pytest`.
- A guard that started failing is a finding. Do not weaken it to make the pass go green.
- Leave `GATE` in `tools/pagespec/__main__.py` alone unless a row is specifically about it.
- The submodules own their pages and their code; this repository re-points them.
