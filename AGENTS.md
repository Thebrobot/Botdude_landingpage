# Bot Dude Landing Page Guide

## Business Context
Bot Dude is a front-facing internet persona and offer under The Brobot LLC. It is not a separate company. The landing page exists to turn personality-driven content into booked calls, demo calls, and qualified form submissions.

## Audience
Primary visitors are home service business owners, especially HVAC, plumbing, roofing, electrical, restoration, landscaping, demolition, and other local service trades.

Most traffic is expected from TikTok, Instagram, Facebook, YouTube Shorts, ads, and campaign links.

## Offer
Keep these offer details exact:

- $3,000 custom setup waived for qualifying businesses.
- $697/month if they keep it.
- No long-term contract.
- Limited monthly build spots.

## Brand Voice
Funny, direct, quirky, practical, and memorable. Credible, but never generic SaaS. Use short sentences and plain language a home service owner would understand.

## Copy Rules
- Do not use em dashes.
- Do not invent testimonials.
- Do not invent customer names.
- Do not invent revenue results.
- Do not invent fake stats or case studies.
- Keep the "no fake stats" honesty visible when relevant.

## Local Workflow
This local folder is the source of truth. Edit only local files in this repo unless the user explicitly says otherwise.

Do not commit, push, deploy, or make remote-only edits without approval.

## Preview And Checks
Preview locally with:

```bash
npm run dev
```

The site should serve at:

```text
http://localhost:3000
```

Useful checks:

```bash
rg -n "\\$3,000|\\$697/month|980-BOT-DUDE|Claim My Free Bot Build" index.html
rg -n "botdude_hero_claim_click|botdude_demo_call_click|botdude_video_play_click|botdude_calculator_used|botdude_form_submit|botdude_mobile_call_click|botdude_mobile_claim_click" index.html
```
