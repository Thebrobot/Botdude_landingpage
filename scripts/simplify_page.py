"""
Simplify the Botdude landing page.

Cuts 6 redundant sections and reorders the remainder into a
7-section funnel:
  1. Hero
  2. Calculator
  3. Solution + How It Works
  4. The Offer
  5. Built Deployments + Trades Bento
  6. Proof Build
  7. FAQ  →  CTA band  →  Claim form
"""

import re, sys
from pathlib import Path

SRC = Path(__file__).parent.parent / "index.html"
OUT = SRC  # overwrite in-place

html = SRC.read_text(encoding="utf-8")

# ── helpers ──────────────────────────────────────────────────────────────────

def extract_section(html: str, section_id: str) -> tuple[str, str]:
    """Return (html_without_section, section_html).

    Handles the case where a section is preceded by an HTML comment.
    """
    # Allow an optional comment line between the blank line and the section tag
    pattern = rf'(\n\n        (?:<!--[^\n]*-->\n        )?)<section id="{re.escape(section_id)}"[^>]*>.*?</section>'
    m = re.search(pattern, html, re.DOTALL)
    if not m:
        print(f"WARNING: section #{section_id} not found", file=sys.stderr)
        return html, ""
    # Keep the leading \n\n spacing but strip any comment
    section_html = "\n\n        " + html[m.start(1) + len(m.group(1))  : m.end()]
    return html[:m.start()] + html[m.end():], section_html


def extract_cta_band(html: str, anchor: str) -> tuple[str, str]:
    """Extract the <div class="cta-band"...> block that follows `anchor`."""
    idx = html.find(anchor)
    if idx == -1:
        return html, ""
    band_start = html.find('\n\n        <div class="cta-band"', idx)
    if band_start == -1:
        return html, ""
    band_end = html.find('</div>\n\n', band_start)
    if band_end == -1:
        return html, ""
    band_end += len('</div>')
    chunk = html[band_start:band_end]
    return html[:band_start] + html[band_end:], chunk


# ── 1. Pull out sections we want to keep and reorder ─────────────────────────

# Remove sections that are being cut entirely
CUT_IDS = ["before-after", "hero-detail", "claim-steps", "compare-paths", "integrations", "additive"]
for sid in CUT_IDS:
    html, removed = extract_section(html, sid)
    print(f"Removed #{sid} ({len(removed)} chars)")

# Extract sections we need to reorder
html, calc_section    = extract_section(html, "calculator")
html, solution_section = extract_section(html, "solution")
html, how_section     = extract_section(html, "how")
html, offer_section   = extract_section(html, "the-offer")
html, built_section   = extract_section(html, "built-deployments")
html, trades_section  = extract_section(html, "trades-bento")
html, proof_section   = extract_section(html, "proof-build")
html, faq_section     = extract_section(html, "faq")
html, claim_section   = extract_section(html, "claim")

# Extract the two cta-band divs (they're not <section> elements)
# First one (after claim form, before calculator) – already gone since claim was extracted
# Find all cta-band divs remaining in html
cta_band_pattern = r'\n\n        <div class="cta-band".*?</div>\n        </div>\n    </div>'
cta_bands = re.findall(cta_band_pattern, html, re.DOTALL)
# Remove all remaining cta-bands from html
html = re.sub(cta_band_pattern, '', html, flags=re.DOTALL)
# We'll use one cta-band at the end (the second one, "Questions about the offer")
final_cta_band = cta_bands[-1] if cta_bands else ""

# ── 2. Reassemble in the new order, inserted right after the hero ─────────────

# Find the end of the hero section
hero_end = html.find('</section>', html.find('<section class="hero'))
hero_end += len('</section>')

# Build the new main content block
new_sections = (
    calc_section +
    solution_section +
    how_section +
    offer_section +
    built_section +
    trades_section +
    proof_section +
    faq_section +
    final_cta_band +
    claim_section
)

html = html[:hero_end] + new_sections + html[hero_end:]

# ── 3. Fix FAQ internal link that pointed to removed #integrations ────────────
html = html.replace(
    'See <a href="#integrations" style="color: var(--primary-orange); font-weight: 700; text-decoration: none; border-bottom: 1px solid rgba(34, 211, 238, 0.35);">CRM &amp; forwarding</a> on this page for a fuller list.',
    'We confirm integrations during your qualification call.'
)

# ── 4. Update footer nav: remove links to cut sections ───────────────────────
# Remove the Compare and Why AI links from the footer
html = html.replace(
    '<a href="#compare-paths">Compare</a>\n                    <span aria-hidden="true"> &nbsp;·&nbsp; </span>\n                    <a href="#additive">Why AI</a>\n                    <span aria-hidden="true"> &nbsp;·&nbsp; </span>\n                    <a href="#faq">FAQ</a>',
    '<a href="#how">How It Works</a>\n                    <span aria-hidden="true"> &nbsp;·&nbsp; </span>\n                    <a href="#faq">FAQ</a>'
)

# ── 5. Write output ───────────────────────────────────────────────────────────
OUT.write_text(html, encoding="utf-8")
print(f"\nDone. Written to {OUT}")
print(f"Final file size: {len(html):,} chars")
