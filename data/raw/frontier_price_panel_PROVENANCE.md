# Frontier price/benchmark panel — provenance

Compiled: 2026-09-23. Companion to `frontier_price_panel.csv`. Per Jeff's
instructions, this replaces the Epoch/AA-scraping approach to C_t with a
hand-curated panel of 17 models, Jan 2023–present, sourced strictly from
each model's own primary announcement/paper/model-card/pricing-doc — never
from Epoch AI or Artificial Analysis (those remain available as a
cross-check per `src/acquisition/epoch_ai.py` and its PROVENANCE, just not
the foundation).

Benchmark: MMLU was chosen over GPQA Diamond because GPQA didn't exist
before Nov 2023 and wasn't commonly reported until ~Feb–Mar 2024 (confirmed:
it's essentially absent from primary sources for GPT-4, Claude 2, and GPT-4
Turbo). **However, this decision was only checked against the front of the
timeline, not the back — see "Systematic issues" below, which surfaced a
real problem with committing to MMLU alone.**

Wayback Machine notes: the `archive.org/wayback/available` endpoint proved
heavily rate-limited (repeated 429s even with backoff); the CDX API
(`web.archive.org/cdx/search/cdx`) worked reliably instead and is what was
used throughout. Anthropic separately publishes dated, content-addressed
pricing PDFs (`www-cdn.anthropic.com/<hash>/model_pricing_<month><year>.pdf`)
for its earliest models — no Wayback snapshot needed for those since the
PDF itself is a permanent, dated primary source.

## Per-row detail beyond what fits in the CSV

**GPT-4 (Mar 2023).** MMLU 86.4% quoted directly from Table 2 of the arXiv
technical report. Price confirmed from the actual archived HTML pricing
table (not a summary): "8K context | $0.03 / 1K tokens (prompt) | $0.06 / 1K
tokens (completion)" — converted to per-million.

**Claude 2 (Jul 2023).** MMLU 78.5% (5-shot CoT) read directly from Table
(Section 4.3) of Anthropic's own Model Card and Evaluations PDF — the
announcement blog post itself does not report MMLU at all. Price: the
announcement says "same price as Claude 1.3" without figures; found
Anthropic's own dated pricing PDF (filename literally
`model_pricing_july2023.pdf`) instead of relying on the announcement.

**GPT-4 Turbo (Nov 2023).** Price verified from an archived pricing-table
fetch, same day as release. MMLU: genuinely not found — OpenAI never
published an updated technical report or system card for the
`gpt-4-1106-preview` model; a "86.5%" figure appears on third-party
aggregator sites with no traceable OpenAI source, so it was **not** used.

**Gemini 1.5 Pro (Feb 2024).** MMLU 81.9% (5-shot) confirmed twice,
independently: once directly from the Gemini 1.5 technical report, and
again by cross-reading it off Anthropic's own Claude 3 model card
comparison table (Table 1), which lists Gemini 1.5 Pro's MMLU as 81.9% too.
Price: **structurally absent** — Google's own Feb 15 2024 announcement says
pricing is "coming soon" and the model was free-tier-only at launch. This is
a real data gap, not an oversight — see "Systematic issues."

**Claude 3 Opus (Mar 2024).** MMLU 86.8% (5-shot) verified by me directly
from Table 1 of the model card PDF (this also cross-confirmed the GPT-4 and
Gemini 1.5 Pro numbers above, and shows Gemini 1.0 Ultra never made it into
this table at all — likely for the same "no stable public API price" reason
as Gemini 1.5 Pro/2.5 Pro). Price confirmed via a same-day archived snapshot
of the announcement page's pricing table.

**GPT-4o (May 2024).** MMLU 87.2% quoted directly ("GPT-4o sets a new
high-score of 87.2% on 5-shot MMLU") from the announcement, archived same
day. Price from a same-day archived pricing-page snapshot, model id
`gpt-4o-2024-05-13`. Price was cut later (commonly reported as $2.50/$10.00)
— that later figure must not be used for this row.

**Claude 3.5 Sonnet (Jun 2024).** MMLU 90.4% (5-shot CoT) from the official
model card addendum PDF. Price quoted directly from the (static) announcement
page.

**o1 (Dec 2024).** MMLU 92.3% (0-shot, English/non-translated row) from
Table 17 of OpenAI's own o1 System Card PDF — o1's primary materials report
MMLU via a multilingual-robustness table rather than a headline capability
table; 92.3% is the directly-comparable English row. Price: model id
`o1-2024-12-17` (API GA date, distinct from the Dec 5 ChatGPT release);
snapshot is from Dec 21 (4 days after API GA) because o1's pricing row
depends on client-side JS that isn't present in the raw HTML of the Dec 17
snapshot — no evidence of a price change in that 4-day gap was found, but
this is slightly less tight than the "same day" sourcing used elsewhere.

**DeepSeek-V3 (Dec 2024).** MMLU 88.5 (EM) from Table 6 of the official
technical report (arXiv:2412.19437). Price confirmed via a same-day archived
snapshot of DeepSeek's pricing docs — but the source page itself states this
is a **discounted/promotional** cache-miss price in effect only through
2025-02-08 16:00 UTC, after which the standard list price ($0.27/M in,
$1.10/M out) took over automatically. Recorded the promotional at-launch
price since that is literally what was true "at release," per Jeff's
instruction to record price as announced at release — flagging prominently
since it's materially different from the standard price.

**DeepSeek-R1 (Jan 2025, mandatory).** MMLU 90.8 (Pass@1) from Table 4 of
the official paper (arXiv:2501.12948). Price confirmed via a snapshot one
day after launch; the source page explicitly states R1 was **not** part of
the V3 launch discount, so this is a genuine standard at-launch price, not a
promotional one. Footnote in the source: CoT/reasoning tokens are billed
identically to output tokens.

**Claude 3.7 Sonnet (Feb 2025).** Price quoted directly from the
announcement (explicitly "includes thinking tokens," stated as unchanged
from 3.5 Sonnet). MMLU: checked both the announcement and the full system
card PDF — the only MMLU mentions in the system card are unrelated (MMLU
questions used as chain-of-thought-faithfulness probes in a safety study,
not a capability score). Genuinely absent, not an extraction failure.

**Gemini 2.5 Pro (Mar 2025).** Both gaps at once: the Mar 25 2025 launch
post states "we'll also introduce pricing in the coming weeks," confirmed
still absent from Google's pricing docs as of Mar 27; first real price
appeared ~Apr 17 2025 (recorded in the notes column, not used as the
release-time figure). MMLU: launch materials emphasize GPQA Diamond, AIME
2025, and Humanity's Last Exam instead — no MMLU reported at all.

**Claude Opus 4 (May 2025).** Price quoted directly from the announcement,
same day. MMLU: the system card reports MMMLU (multilingual MMLU) = 87.4%
instead of vanilla MMLU — a related but distinct benchmark, not substituted
into the MMLU column.

**GPT-5 (Aug 2025).** Price confirmed via same-day archived pricing
snapshot. MMLU: the GPT-5 system card PDF only contains a per-language
multilingual-MMLU table, no single overall number; a "92.5% MMLU" figure
circulates on a third-party leaderboard (llm-stats.com) and was deliberately
**not** used.

**Claude Opus 4.5 (Nov 2025).** Price quoted directly from the announcement,
archived same day. MMLU: system card reports MMMLU = 90.8% and GPQA Diamond
= 87.0% instead of vanilla MMLU — neither substituted in.

**DeepSeek-V4-Pro (Apr 2026, event anchor).** Confirmed as a real model via
its own arXiv technical report (arXiv:2606.19348) and DeepSeek's own docs —
not a hallucinated post-cutoff entry. Price confirmed via a same-day
archived pricing snapshot. MMLU: the tech report reports MMLU-Pro, and a
clean model-specific number for base "V4-Pro" (as opposed to a
"V4-Pro-Max" high-reasoning-effort variant discussed in the same paper)
could not be extracted — left blank. DeepSeek's live (Sept 2026) pricing has
since moved to a peak/off-peak split structure, materially different from
the April launch price recorded here.

**GPT-5.5 (Apr 2026, confound — coincides with DeepSeek-V4-Pro).** Confirmed
real via OpenAI's own announcement (live page 403s, so sourced via a
same-day archived snapshot) plus independent corroboration. No MMLU or
classic knowledge benchmark reported at all — SWE-Bench Pro, Terminal-Bench
2.0, and FrontierMath tiers are what OpenAI emphasizes for this release.

## Systematic issues surfaced — not resolved, needs a decision

1. **MMLU coverage collapses from ~Feb 2025 onward.** 7 of 17 models (GPT-4
   Turbo, Claude 3.7 Sonnet, Gemini 2.5 Pro, Claude Opus 4, GPT-5, Claude
   Opus 4.5, DeepSeek-V4-Pro) have no usable primary-sourced MMLU score —
   either it's genuinely not reported, or (Opus 4/4.5) a different
   benchmark (MMMLU, GPQA Diamond) is reported instead. This isn't random
   noise: starting in 2025, OpenAI, Anthropic, and DeepSeek's flagship
   launches consistently report GPQA Diamond, MMLU-Pro, or MMMLU instead of
   vanilla MMLU. The original benchmark-coverage check only tested the
   front of the timeline (correctly found GPQA absent pre-Nov-2023) and
   should have also checked the back before committing — it didn't, and
   this is the result. GPQA Diamond likely has the mirror-image problem
   (probably good coverage 2024–2026, zero coverage before Nov 2023).
   Neither benchmark covers the full Jan 2023–present span cleanly.

2. **Two models have no price at release at all**, not just a missing
   number: Gemini 1.5 Pro and Gemini 2.5 Pro were both launched as free
   previews with pricing announced weeks later. This looks like a Google
   pattern specifically (both instances), not a one-off.
