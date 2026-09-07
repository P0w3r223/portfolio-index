"""Where each published surface's bytes come from — the I/O boundary, and nothing else.

Eleven repositories publishing twelve surfaces, **three different kinds of source**, and
getting this wrong is the failure `0007` §2 calls the one every earlier attempt made:
answering a question about the rendered page from something that is not the rendered page.

- Ten commit a `docs/index.html` served byte-identically. Read the file.
- `car-price-ml` commits a **second** surface, `docs/app/index.html` — hand-written inside a
  repository that generates and byte-diffs everything else.
- `wroclaw-air-insights` commits **no HTML at all** (`.gitignore:25`). Its page is a Pages
  artifact rebuilt daily, so it exists only at the live URL. Reading `reports/site/` gets an
  untracked local build that has been 24 days stale and produced a wrong answer that survived
  a session.
- `token-budget` has no page. It is the twelfth repository, is not a surface, and is not
  checked — which is why the repository count here is eleven and not twelve.
"""

from __future__ import annotations

import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from . import render

USER_AGENT = "pagespec (portfolio conformance checker)"
FETCH_TIMEOUT = 30


@dataclass(frozen=True)
class Surface:
    """One published page: what to call it, and where its bytes are."""

    name: str
    repo: str
    path: str | None = None
    url: str | None = None
    note: str = ""

    @property
    def must_fetch(self) -> bool:
        return self.path is None


SURFACES: tuple[Surface, ...] = (
    Surface("ab-lab", "ab-lab", "docs/index.html"),
    Surface("apply-scout", "apply-scout", "docs/index.html"),
    Surface("auth-log-scan", "auth-log-scan", "docs/index.html"),
    Surface("car-price-ml", "car-price-ml", "docs/index.html"),
    Surface("car-price-ml/app", "car-price-ml", "docs/app/index.html",
            note="hand-written; the only surface here CI does not byte-diff"),
    Surface("doc-extract", "doc-extract", "docs/index.html"),
    Surface("it-job-radar", "it-job-radar", "docs/index.html"),
    Surface("mini-traceroute", "mini-traceroute", "docs/index.html",
            note="the one page whose CSS is not inlined"),
    Surface("mlops-car-price", "mlops-car-price", "docs/index.html"),
    Surface("pl-jobs-lora", "pl-jobs-lora", "docs/index.html"),
    Surface("pl-review-sense", "pl-review-sense", "docs/index.html"),
    Surface("wroclaw-air-insights", "wroclaw-air-insights",
            url="https://p0w3r223.github.io/wroclaw-air-insights/",
            note="commits no HTML; live URL is the only surface that exists"),
)


@dataclass
class Loaded:
    """A surface's markup and its complete stylesheet, with what could not be read."""

    surface: Surface
    html: str
    css: str
    stylesheets: list[str] = field(default_factory=list)
    unreadable: list[str] = field(default_factory=list)


def _fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT) as response:
        return response.read().decode("utf-8", errors="replace")


def load(surface: Surface, root: Path, *, allow_fetch: bool,
         errors: dict[str, str] | None = None) -> Loaded | None:
    """The surface's markup, or `None` when it cannot be read.

    Returning `None` rather than an empty page matters: an empty page satisfies no clause and
    would be reported as thirteen failures, which reads as a portfolio-wide regression when
    the truth is that the network was off.
    """
    if surface.must_fetch:
        if not allow_fetch:
            return None
        try:
            html = _fetch(surface.url)
        except Exception as error:
            # The exception text, not just the fact. Since `0008` S-gate the scheduled job
            # is the only reader of this surface and it now gates, so `fetch failed` is a
            # thing somebody has to act on — and a 404 (the page is gone, a real regression)
            # and a DNS blip are the same line without this. Recorded on the surface rather
            # than raised, because a page that cannot be read must not stop the other eleven
            # from being reported.
            if errors is not None:
                errors[surface.name] = f"{type(error).__name__}: {error}"
            return None
        return _with_styles(surface, html, base_url=surface.url)

    page_path = root / surface.repo / surface.path
    if not page_path.is_file():
        return None
    # `errors="replace"`, matching the fetch path above: one undecodable byte in one
    # page must not end the run for the other eleven.
    html = page_path.read_text(encoding="utf-8", errors="replace")
    return _with_styles(surface, html, base_path=page_path)


def _with_styles(surface: Surface, html: str, *, base_path: Path | None = None,
                 base_url: str | None = None) -> Loaded:
    """Inline `<style>` blocks plus every same-origin `<link>`ed sheet, concatenated.

    Reading only the inline blocks is the trap that recorded `mini-traceroute` as having no
    `overflow-x` rule across three sessions, so the external sheets are not optional and a
    sheet that cannot be read is reported rather than skipped.
    """
    page = render.parse(html)
    parts = list(page.inline_styles)
    names: list[str] = ["<style>"] * len(page.inline_styles)
    unreadable: list[str] = []

    for href in page.stylesheet_hrefs():
        if href.startswith(("http://", "https://", "//")):
            unreadable.append(f"{href} (third party, not read)")
            continue
        try:
            if base_path is not None:
                parts.append((base_path.parent / href).read_text(
                    encoding="utf-8", errors="replace"))
            else:
                parts.append(_fetch(urllib.parse.urljoin(base_url, href)))
            names.append(href)
        except Exception:
            unreadable.append(href)

    return Loaded(surface, html, "\n".join(parts), names, unreadable)
