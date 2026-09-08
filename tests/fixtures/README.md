# Fixtures of record

Every file here is a **reduction of a real published page**, cut down to the markup or the
stylesheet that demonstrates one recorded defect, and then **frozen**. The provenance is the
point: each is the page that actually bit, so the regression it guards cannot be retired by
accident.

They are committed rather than read live out of the sibling working trees, and that boundary
is deliberate. A test that reads `pl-review-sense/docs/index.html` goes red the day
`pl-review-sense` legitimately edits a table — a false red, and a false red that recurs is
eventually silenced. The live trees are swept separately in `test_published_surfaces.py`,
and that sweep asserts only what survives a page being rewritten.

| fixture | reduced from | at | demonstrates |
|---|---|---|---|
| `svg_titles.html` | `ab-lab/docs/index.html` | `802dd78`, 2026-09-04 | an SVG `<title>` shadowing the document's, so the page is named after its last chart |
| `welded_cells.html` | `pl-review-sense/docs/index.html` | `87f43db`, 2026-09-04 | adjacent `<td>` welding into a grouped figure the page does not print |
| `narrow_spaces.html` | `doc-extract/docs/index.html` | `4e42ca3`, 2026-09-04 | `U+202F` and `U+00A0` separators, which `str.split()` rewrites to plain spaces |
| `house_palette.css` | `doc-extract/docs/index.html` | `4e42ca3`, 2026-09-04 | a `prefers-color-scheme: dark` block whose declarations leak into light when only its header is removed |
| `mini_traceroute_shape/` | `mini-traceroute/docs/` | `19cda5f`, 2026-09-05 | the one page whose CSS is not inlined — the scroller rule lives in an external sheet |
| `data_driven_alpha.html` | `pl-review-sense/docs/index.html` | `6f908ec`, 2026-09-08 | alpha as a **presentation attribute**, one value per cell from the data, with two text labels drawn over it — invisible to a clause reading only the stylesheet, and the page it came from was failing SC 1.4.3 on the second label |
| `wroclaw_scroller.css` | `https://p0w3r223.github.io/wroclaw-air-insights/` | fetched 2026-09-05 | the table made its own scroller, so there is no scrolling *ancestor* to walk up to |

Refreshing one of these is a deliberate act: re-cut it from the named source, update the row
above, and confirm the test still fails when the fix it guards is reverted. A fixture that no
longer demonstrates its defect is worse than no fixture at all.
