# ADR 0002 — P5 corpus: synthetic from the KSeF schema, plus a small real held-out set

Date: 2026-08-18
Status: accepted
Author: Piotr Cząstkiewicz
Related to: [0001_p5-doc-extract-thesis.md](0001_p5-doc-extract-thesis.md), [0003_p5-metric-design.md](0003_p5-metric-design.md)

---

## Context

P5 needs Polish invoices with trustworthy ground truth. Neither half of that is easy.

**Real invoices cannot be committed.** They carry NIP numbers, addresses, bank accounts and
amounts — personal and commercial data under RODO. A portfolio repository is public.

**There is no usable public Polish invoice corpus.** SROIE, CORD, DocILE and FUNSD are English or
Indonesian, and mostly receipts or forms rather than Polish VAT invoices with the fields that make
the domain interesting.

**And borrowed gold is exactly what capped P4.** `pl-jobs-lora` scores against scraped platform
metadata: free, noisy, and demonstrably the ceiling of the metric — best field F1 in the committed
table is 0.39 and a frontier model reaches 0.28 on `tech_expected`, which reads as a gold-quality
ceiling rather than a model ceiling. Repeating that mistake in a new domain would undercut P5's
entire thesis, which depends on being able to tell extraction error from label error.

## Decision

**A synthetic generator built on the official KSeF invoice schema, plus a small real held-out set
that is annotated but never committed.**

### The synthetic side

The Polish Ministry of Finance publishes the XSD for the structured invoice (`FA`) used by KSeF,
the national e-invoicing system, which became mandatory during 2026. The generator emits a
**schema-conformant XML → renders it to PDF**; the extractor's job is to recover the fields.

### Verified at source, 2026-08-18

The prerequisite flagged below has been resolved — every fact here comes from the Ministry's own
published artifacts, not from recollection:

| Fact | Value |
|---|---|
| Schema in force | **FA(3)**, since 2026-02-01 (it replaced FA(2), which applied through 2026-01-31) |
| Canonical XSD | `http://crd.gov.pl/wzor/2025/06/25/13775/schemat.xsd` (published 2025-06-25, 184 KB) |
| Fixed schema attributes | `kodSystemowy="FA (3)"`, `wersjaSchemy="1-0E"` |
| Mandate | 2026-02-01 for taxpayers whose 2024 sales exceeded 200 M PLN; 2026-04-01 for everyone else; taxpayers under 10 k PLN/month may defer *issuing* to end-2026 but must *receive* from 2026-02-01 |
| `RodzajFaktury` | closed enum: `VAT`, `KOR`, `ZAL`, `ROZ`, `UPR`, `KOR_ZAL`, `KOR_ROZ` |
| `TStawkaPodatku` | closed enum: `23`, `22`, `8`, `7`, `5`, `4`, `3`, `0 KR`, `0 WDT`, `0 EX`, `zw`, `oo`, `np I`, `np II` |
| Monetary type | `TKwotowy` = `xsd:decimal`, `totalDigits=18`, `fractionDigits=2` |
| Unit-price type | `TKwotowy2` = `xsd:decimal`, `totalDigits=22`, **`fractionDigits=8`** |

Two of these change the project rather than merely confirming it.

**The XSD contains zero `xsd:assert` elements.** It is XSD 1.0, so it can express types,
enumerations and cardinality — and nothing else. Not one arithmetic or cross-field relationship is
validated: `P_15` (gross total) is simply a decimal, unconstrained by `P_13_*` (net by rate) or
`P_14_*` (VAT by rate), and line-level `P_11`/`P_11Vat` are unconstrained by either. **The national
standard defines the shape of an invoice and leaves every consistency rule unenforced.** That gap
is precisely where [0001](0001_p5-doc-extract-thesis.md)'s pillars 1 and 2 live: the invariants are
genuinely additive engineering, not a re-implementation of validation the schema already performs.
Anyone claiming "just validate against the official XSD" can be answered with the file itself.

**Rounding is forced by the schema's own types, not contrived.** Unit price `P_9A` carries eight
decimal places while every total carries two, so `P_8B × P_9A` generally does not land on a
2-decimal boundary. The grosz-rounding difficulty tier is therefore a property of the standard, and
the tolerance band in the invariants has to be derived rather than guessed.

`RodzajFaktury` also confirms the difficulty tiers below were the right ones: `KOR`, `ZAL` and
`ROZ` are first-class document kinds in the standard, each with its own amount semantics.

Three consequences, each answering a specific weakness found in the sibling projects:

1. **Gold is the source XML.** Generation and ground truth come from one artifact, so labels are
   exact and free. This is the direct fix for P4's ceiling problem — there is no annotation noise
   to confound with model error.
2. **Difficulty becomes a controlled variable.** The generator deliberately produces the hard
   cases, in named tiers: mixed VAT rates within one document, a correction invoice (`korekta`)
   with negative amounts, an advance invoice (`zaliczka`), reverse charge, split-payment mechanism,
   foreign currency with an NBP rate, rounding on the grosz boundary, and line items continuing
   onto a second page. Accuracy can then be plotted **against document difficulty** — something no
   scraped corpus offers.
3. **The target schema is not invented.** Modelling a subset of the national standard is more
   credible than modelling a schema of my own design, and it dates the project to a live
   regulatory change.

### The real side

**20–40 real invoices, hand-annotated, not committed.** The repository holds annotations, content
hashes and the reproduction procedure — never the documents. Both numbers are reported side by
side, and **the gap between them is itself a result.**

## Alternatives considered

| Option | Why rejected |
|---|---|
| Synthetic only | Faster and free of any RODO question, corpus fully reproducible from a seed. But the obvious objection — *"this only works on documents you generated yourself"* — is left unanswered, because there is nothing to compare against. |
| Real invoices only | Maximum credibility of the result, but gold must be hand-annotated (expensive, and it becomes the metric's ceiling — precisely P4's failure), the corpus would be a few dozen documents, and the repository cannot contain them. |
| An existing public corpus (SROIE / CORD / DocILE) | Wrong language, wrong document type, and none carry the Polish domain invariants (NIP checksum, split payment, the `korekta` semantics) on which the entire thesis rests. |

## Consequences

- ~~**Verification is a blocking prerequisite for M1.**~~ **Resolved 2026-08-18** — see the table
  above. FA(3) is the target; the XSD is pinned to the CRWD URL and should be vendored into the repo
  with its retrieval date, so the model is reproducible even if the Ministry republishes.
- **The generator is a first-class engineered artifact**, not a test fixture. It gets its own
  tests, its own difficulty taxonomy, and a documented seed so the corpus is reproducible.
- **The synthetic corpus does not cover real-world visual chaos** — skew, stamps, handwriting,
  poor scans, layouts no template anticipated. This limit is stated in the README, not discovered
  by a reviewer. The real held-out set exists precisely to measure how large it is.
- The synthetic↔real gap may be large. If it is, that is the finding and it gets reported; a
  project whose headline requires the gap to be small is a project structured to be dishonest.
- Because gold is exact, **label noise is removed as a confound** — which is what makes the
  detector study in [0001](0001_p5-doc-extract-thesis.md) pillar 2 interpretable at all.
- The real set must be re-derivable by its owner but by nobody else. The procedure (which
  invoices, how redacted, how annotated) is documented; the artifacts are not published.
