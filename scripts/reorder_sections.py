#!/usr/bin/env python3
"""
Reorder landing page sections for optimal mobile conversion flow.

New order (before form):
  1. Hero (unchanged)
  2. Before/After  <- moved up from position 5
  3. Solution      <- moved up from position 4
  4. The Offer     <- moved up from position 7
  5. How It Works  <- moved
  6. Why Bot Dude  <- moved
  7. Claim Steps   <- moved up from near end
  8. Claim Form    <- moved up from end

Below the form (objection zone):
  9.  CTA band "Ready to move"
  10. Calculator
  11. Built Deployments showcase
  12. Trades bento
  13. Proof Build / No Fake Stats
  14. Compare Paths
  15. Integrations
  16. Additive Value
  17. FAQ
  18. CTA band "Questions about the offer"

Removed:
  - #problem stat cards (redundant with before/after)
  - inline CTA band pointing to calculator (orphaned after reorder)
  - #who section (redundant with trades bento)
"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def block(start_1, end_1):
    """Return lines[start_1-1 : end_1] (1-indexed, inclusive)."""
    return lines[start_1 - 1 : end_1]

NL = ['\n']

# ── Confirmed line ranges (1-indexed, inclusive) ──────────────────────────────
HERO_END          = 3649   # </section> for hero

PROBLEM_S         = 3651;  PROBLEM_E         = 3673   # REMOVED
CTA_CALC_S        = 3675;  CTA_CALC_E        = 3683   # REMOVED
CALCULATOR_S      = 3686;  CALCULATOR_E      = 3764
SOLUTION_S        = 3767;  SOLUTION_E        = 3817
BEFORE_AFTER_S    = 3820;  BEFORE_AFTER_E    = 3948
HOW_S             = 3950;  HOW_E             = 3976
THE_OFFER_S       = 3979;  THE_OFFER_E       = 4001
HERO_DETAIL_S     = 4004;  HERO_DETAIL_E     = 4038
TRADES_BENTO_S    = 4040;  TRADES_BENTO_E    = 4141
BUILT_DEPLOY_S    = 4144;  BUILT_DEPLOY_E    = 4197
INTEGRATIONS_S    = 4199;  INTEGRATIONS_E    = 4235
COMPARE_S         = 4237;  COMPARE_E         = 4266
PROOF_S           = 4268;  PROOF_E           = 4294
ADDITIVE_S        = 4297;  ADDITIVE_E        = 4326
WHO_S             = 4328;  WHO_E             = 4347   # REMOVED
CTA_READY_S       = 4349;  CTA_READY_E       = 4357
FAQ_S             = 4360;  FAQ_E             = 4472
CTA_QUESTIONS_S   = 4475;  CTA_QUESTIONS_E   = 4483
CLAIM_STEPS_S     = 4485;  CLAIM_STEPS_E     = 4512
CLAIM_FORM_S      = 4515;  CLAIM_FORM_E      = 4570
MAIN_CLOSE        = 4571   # </main> starts here
# ─────────────────────────────────────────────────────────────────────────────

part1 = lines[0:HERO_END]          # lines 1–3649 (hero through hero's </section>)
part3 = lines[MAIN_CLOSE - 1:]     # </main>, sales-dock, footer, scripts

new_middle = (
    NL + block(BEFORE_AFTER_S,  BEFORE_AFTER_E)  +
    NL + block(SOLUTION_S,      SOLUTION_E)       +
    NL + block(THE_OFFER_S,     THE_OFFER_E)      +
    NL + block(HOW_S,           HOW_E)            +
    NL + block(HERO_DETAIL_S,   HERO_DETAIL_E)    +
    NL + block(CLAIM_STEPS_S,   CLAIM_STEPS_E)    +
    NL + block(CLAIM_FORM_S,    CLAIM_FORM_E)     +
    # ── objection zone ──────────────────────────────────
    NL + block(CTA_READY_S,     CTA_READY_E)      +
    NL + block(CALCULATOR_S,    CALCULATOR_E)     +
    NL + block(BUILT_DEPLOY_S,  BUILT_DEPLOY_E)   +
    NL + block(TRADES_BENTO_S,  TRADES_BENTO_E)   +
    NL + block(PROOF_S,         PROOF_E)          +
    NL + block(COMPARE_S,       COMPARE_E)        +
    NL + block(INTEGRATIONS_S,  INTEGRATIONS_E)   +
    NL + block(ADDITIVE_S,      ADDITIVE_E)       +
    NL + block(FAQ_S,           FAQ_E)            +
    NL + block(CTA_QUESTIONS_S, CTA_QUESTIONS_E)
)

content = ''.join(part1 + new_middle + NL + part3)

# ── CTA label standardization ─────────────────────────────────────────────────
content = content.replace('>Start My Free Build<', '>Claim My Free Bot Build<')
content = content.replace('>Book the Build Call<', '>Claim My Free Bot Build<')

# ── Section heading improvements for mobile scanning ─────────────────────────
# Before/After: make the H2 scannable at a glance
content = content.replace(
    '<span class="section-label">FIELD_COMPARE_MODE</span>',
    '<span class="section-label">SEE THE DIFFERENCE</span>'
)
content = content.replace(
    'class="headline" style="text-align: center;">LIFE_BEFORE_VS_AFTER<br><i>AGENT_BROSKI.</i>',
    'class="headline" style="text-align: center;">ONE RING.<br><i>TWO OUTCOMES.</i>'
)

# The Offer: drop the self-referential label
content = content.replace(
    '<span class="section-label">WHY THIS OFFER IS HERE</span>',
    '<span class="section-label">THE OFFER</span>'
)

# ─────────────────────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

original_lines = len(lines)
new_lines = content.count('\n')
print(f"Done. Original: {original_lines} lines → New: {new_lines} lines")
print(f"Removed sections: #problem ({PROBLEM_E - PROBLEM_S + 1} lines), "
      f"cta-calc-band ({CTA_CALC_E - CTA_CALC_S + 1} lines), "
      f"#who ({WHO_E - WHO_S + 1} lines)")
