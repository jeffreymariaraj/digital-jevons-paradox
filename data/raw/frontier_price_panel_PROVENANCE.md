# Frontier price/benchmark panel — provenance

Compiled: 2026-09-23. Companion to `frontier_price_panel.csv`. Per Jeff's
instructions, this replaces the Epoch/AA-scraping approach to C_t with a
hand-curated panel of models, Jan 2023–present, sourced strictly from each
model's own primary announcement/paper/model-card/pricing-doc — never from
Epoch AI or Artificial Analysis (those remain available as a cross-check
per `src/acquisition/epoch_ai.py` and its PROVENANCE, just not the
foundation). 15 models survived to the final panel (17 were researched;
Gemini 1.5 Pro and Gemini 2.5 Pro were dropped — see "Decisions made"
below).

Benchmark: MMLU was chosen over GPQA Diamond because GPQA didn't exist
before Nov 2023 and wasn't commonly reported until ~Feb–Mar 2024 (confirmed:
it's essentially absent from primary sources for GPT-4, Claude 2, and GPT-4
Turbo). **This check only covered the front of the timeline, not the
back — see "Decisions made" below**, which documents a real problem this
caused (MMLU coverage collapses from ~Feb 2025 onward) and how it was
resolved: MMLU stays the committed primary column; a secondary column
records whatever capability benchmark each gap model's own materials
actually report, clearly labeled and never treated as a substitute.

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

**Gemini 1.5 Pro (Feb 2024) — DROPPED from the final panel.** MMLU 81.9%
(5-shot) was confirmed twice, independently: once directly from the Gemini
1.5 technical report, and again by cross-reading it off Anthropic's own
Claude 3 model card comparison table (Table 1), which lists Gemini 1.5
Pro's MMLU as 81.9% too. But price was **structurally absent** — Google's
own Feb 15 2024 announcement says pricing is "coming soon" and the model
was free-tier-only at launch. Jeff's decision: drop rather than use a
weeks-later price or substitute a different model. Kept in this provenance
doc (not in the CSV) so nobody re-adds it without knowing why.

**Claude 3 Opus (Mar 2024).** MMLU 86.8% (5-shot) verified by me directly
from Table 1 of the model card PDF (this also cross-confirmed the GPT-4 and
Gemini 1.5 Pro numbers above, and shows Gemini 1.0 Ultra never made it into
this table at all — likely for the same "no stable public API price" reason
as Gemini 1.5 Pro/2.5 Pro). Price confirmed via a same-day archived snapshot
of the announcement page's pricing table. The same Table 1 also reports
GPQA Diamond (0-shot CoT) = 50.4% for Opus — recorded as the secondary
benchmark column even though not needed here, since it comes from the same
primary table and turned out useful later for the MMLU/GPQA crosswalk check
(see "Decisions made").

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
technical report (arXiv:2412.19437). This same table also reports GPQA
Diamond (Pass@1) = 59.1 for V3, alongside 6 other contemporary models
evaluated under identical methodology — recorded as the secondary
benchmark, and this table turned out to be the key evidence for the
MMLU/GPQA crosswalk check (see "Decisions made"). Price confirmed via a
same-day archived snapshot of DeepSeek's pricing docs — but the source page
itself states this is a **discounted/promotional** cache-miss price in
effect only through 2025-02-08 16:00 UTC, after which the standard list
price ($0.27/M in, $1.10/M out) took over automatically. Recorded the
promotional at-launch price since that is literally what was true "at
release," per Jeff's instruction to record price as announced at release —
flagging prominently since it's materially different from the standard
price.

**DeepSeek-R1 (Jan 2025, mandatory).** MMLU 90.8 (EM) from Table 3 of the
official paper (arXiv:2501.12948) — the fork that found this cited it as
"Table 4, Pass@1"; on direct inspection it's actually Table 3 and the MMLU
row is EM, not Pass@1 (GPQA Diamond is the Pass@1 row) — corrected here.
The same table gives GPQA Diamond (Pass@1) = 71.5 for the final R1, plus
intermediate values for R1-Zero/Dev1/Dev2/Dev3, recorded as the secondary
benchmark. Price confirmed via a snapshot one day after launch; the source
page explicitly states R1 was **not** part of the V3 launch discount, so
this is a genuine standard at-launch price, not a promotional one. Footnote
in the source: CoT/reasoning tokens are billed identically to output
tokens.

**Claude 3.7 Sonnet (Feb 2025).** Price quoted directly from the
announcement (explicitly "includes thinking tokens," stated as unchanged
from 3.5 Sonnet). MMLU: checked both the announcement and the full system
card PDF — the only MMLU mentions in the system card are unrelated (MMLU
questions used as chain-of-thought-faithfulness probes in a safety study,
not a capability score). Followed up by checking GPQA too, specifically for
the secondary-benchmark column: same situation — the system card's only
GPQA mentions (page ~1059 of the PDF) are the same CoT-faithfulness probe
context, not a capability score, and the announcement links out to a
separate "visible-extended-thinking" research post for GPQA/AIME numbers
that was not chased down. This model has no usable secondary benchmark
either — a genuine total gap, not an extraction failure.

**Gemini 2.5 Pro (Mar 2025) — DROPPED from the final panel.** Both gaps at
once: the Mar 25 2025 launch post states "we'll also introduce pricing in
the coming weeks," confirmed still absent from Google's pricing docs as of
Mar 27; first real price appeared ~Apr 17 2025. MMLU: launch materials
emphasize GPQA Diamond, AIME 2025, and Humanity's Last Exam instead — no
MMLU reported at all. Same fate as Gemini 1.5 Pro and the same decision:
dropped rather than using a weeks-later price. Kept here, not in the CSV.

**Claude Opus 4 (May 2025).** Price quoted directly from the announcement,
same day. MMLU: the system card reports MMMLU (multilingual MMLU) = 87.4%
instead of vanilla MMLU — recorded as the secondary benchmark, clearly
labeled as a different (multilingual) variant, not a drop-in substitute.

**GPT-5 (Aug 2025).** Price confirmed via same-day archived pricing
snapshot. MMLU: the GPT-5 system card PDF only contains a per-language
multilingual-MMLU table, no single overall number; a "92.5% MMLU" figure
circulates on a third-party leaderboard (llm-stats.com) and was deliberately
**not** used. For the secondary-benchmark column: the announcement page
(archived) does include a "GPQA Diamond, PhD-level science questions" chart
comparing GPT-5 pro / GPT-5 / OpenAI o3 / GPT-4o, confirming GPT-5 reports
GPQA Diamond — but the exact numeric value could not be reliably pulled
from the page's embedded Vega-Lite chart spec (candidate values [89.4, 88.4,
87.3, 7.9, 77.8, 83.3, 70.1] extracted near the chart definition don't map
cleanly 1:1 onto the 7 compared model/tool-setting combinations, and one
value, 7.9, is clearly not a percentage in this range — likely chart-layout
metadata leaking into the same JSON blob). Left blank rather than guess
which number belongs to plain "GPT-5." Someone spot-checking this row
should view the rendered chart directly rather than trust a scraped number.

**Claude Opus 4.5 (Nov 2025).** Price quoted directly from the announcement,
archived same day. MMLU: system card reports MMMLU = 90.8% and GPQA Diamond
= 87.0%. GPQA Diamond recorded as the secondary benchmark (more standard/
comparable across labs than MMMLU); MMMLU noted but not recorded in a
column.

**DeepSeek-V4-Pro (Apr 2026, event anchor).** Confirmed as a real model via
its own arXiv technical report (arXiv:2606.19348) and DeepSeek's own docs —
not a hallucinated post-cutoff entry. Price confirmed via a same-day
archived pricing snapshot. MMLU: the tech report reports MMLU-Pro (recorded
as the secondary benchmark name), but a clean model-specific number for
base "V4-Pro" (as opposed to a "V4-Pro-Max" high-reasoning-effort variant
discussed in the same paper) could not be extracted — left blank rather
than guessing. DeepSeek's live (Sept 2026) pricing has since moved to a
peak/off-peak split structure, materially different from the April launch
price recorded here.

**GPT-5.5 (Apr 2026, confound — coincides with DeepSeek-V4-Pro).** Confirmed
real via OpenAI's own announcement (live page 403s, so sourced via a
same-day archived snapshot) plus independent corroboration. No MMLU or
classic knowledge benchmark of any kind (including GPQA) reported anywhere
in the announcement — SWE-Bench Pro, Terminal-Bench 2.0, and FrontierMath
tiers are what OpenAI emphasizes for this release. No secondary benchmark
recovered — a genuine total gap.

## Decisions made

**1. MMLU coverage collapses from ~Feb 2025 onward — resolved.** 7 of 17
researched models (GPT-4 Turbo, Claude 3.7 Sonnet, Gemini 2.5 Pro [since
dropped], Claude Opus 4, GPT-5, Claude Opus 4.5, DeepSeek-V4-Pro) have no
usable primary-sourced vanilla MMLU score — either genuinely not reported,
or a different benchmark (MMMLU, GPQA Diamond, MMLU-Pro) is reported
instead. This isn't random: starting in 2025, OpenAI, Anthropic, and
DeepSeek's flagship launches consistently move to GPQA Diamond, MMLU-Pro,
or MMMLU instead of vanilla MMLU. The original benchmark-coverage check
only tested the front of the timeline (correctly found GPQA absent
pre-Nov-2023) and should have also checked the back before committing to
MMLU — it didn't, and this section is the result.

Before deciding how to handle it, checked whether a reliable MMLU→GPQA
crosswalk could be calibrated from models reporting both, per Jeff's
request. Found two genuinely useful overlap tables — both evaluate multiple
models under one consistent internal methodology (more reliable for a
crosswalk than mixing labs' own self-reported numbers, which use different
shot-counts/CoT settings and aren't mutually comparable to begin with):

DeepSeek-V3 paper, Table 6 (non-reasoning models):

| Model | MMLU (EM) | GPQA-Diamond (Pass@1) |
|---|---|---|
| DeepSeek-V2-0506 | 78.2 | 35.3 |
| DeepSeek-V2.5-0905 | 80.6 | 41.3 |
| Qwen2.5-72B-Inst | 85.3 | 49.0 |
| GPT-4o-0513 | 87.2 | 49.9 |
| LLaMA-3.1-405B-Inst | 88.6 | 51.1 |
| DeepSeek-V3 | 88.5 | 59.1 |
| Claude-3.5-Sonnet-1022 | 88.3 | 65.0 |

DeepSeek-R1 paper, Table 3 (R1 development stages):

| Model | MMLU (EM) | GPQA-Diamond (Pass@1) |
|---|---|---|
| R1-Zero | 88.8 | 75.8 |
| R1-Dev1 | 89.1 | 66.1 |
| R1-Dev2 | 91.2 | 70.7 |
| R1-Dev3 | 91.0 | 71.2 |
| R1 (final) | 90.8 | 71.5 |

**Conclusion: no reliable crosswalk exists in the region that matters.**
MMLU is saturating exactly where nearly every 2024–2026 flagship sits
(86–91%), while GPQA-Diamond still spans 35–76 across that same narrow MMLU
band. Worse, reasoning models sit systematically above non-reasoning models
at the same MMLU level (Claude-3.5-Sonnet 88.3/65.0 vs. GPT-4o 87.2/49.9;
DeepSeek-R1 90.8/71.5 vs. GPT-4o 87.2/49.9). A single mapping would carry
roughly ±15–20 points of GPQA-equivalent uncertainty precisely where
threshold-clearing needs to be reliable for the DeepSeek-V4 event window —
Jeff's own bar for whether this was worth doing. Decision: **use the
fallback** — MMLU stays the sole committed/primary column across the whole
panel; a `secondary_benchmark_*` column set in the CSV records whatever
capability benchmark each gap model's own materials actually report
(GPQA Diamond, MMMLU, or MMLU-Pro, each clearly labeled), never used as a
silent substitute; the MMLU-saturation/benchmark-shift problem should be
documented as an explicit limitation in the paper's Methods, in the same
spirit as DATA_PIPELINE.md Section 7's other "known weaknesses."

**2. Gemini 1.5 Pro and Gemini 2.5 Pro have no price at release —
resolved.** Both launched as free previews with pricing announced weeks
later; this looks like a deliberate Google pattern (both instances,
~2.5 months apart in different product cycles), not a one-off oversight.
Decision: **drop both rows** from the panel rather than use a weeks-later
price or hunt for substitute models — the panel dropped from 17 to 15
models as a result, still within the requested 15–25 range. Both are kept
in this provenance doc, not the CSV, so nobody re-adds them later without
knowing why.
