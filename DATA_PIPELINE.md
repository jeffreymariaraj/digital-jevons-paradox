# Data Pipeline: Densing Law / Digital Jevons Paradox

## 1. Series definitions (map to Section 2 of the paper)

| Symbol | Definition | Frequency needed |
|---|---|---|
| C_t | Price per M tokens at a fixed capability threshold | Monthly (macro), weekly (event windows) |
| D_t | Aggregate token volume at that threshold | Monthly (macro), weekly (event windows) |
| X_t | Controls: developer population, enterprise adoption, compute capacity | Monthly/quarterly |
| Z_t | Instrument: accelerator generation cost-per-FLOP, open-weight release dummies | Irregular (event dates) |

## 2. Sources and access method

### C_t — Epoch AI (primary)
- URL: epochai.org/data — "Notable AI Models" and inference-price trend datasets ship as downloadable CSV/Parquet.
- Fields needed: model name, release date, benchmark scores (pick ONE composite and hold it fixed across the whole series), input price/M tokens, output price/M tokens.
- Construction: for each month t, C_t = min over {models released by t, benchmark >= threshold tau} of blended price (0.75*input + 0.25*output, per Section 3.2's assumption — sensitivity-test this ratio in step 8).
- **Decide tau explicitly and document it in the paper's Methods** — this single choice drives the whole series.

### C_t — Artificial Analysis (cross-check)
- No public bulk export as of this writing; the intelligence-index and pricing pages are scrapeable (requests + BeautifulSoup, respect robots.txt and rate limits).
- For historical points before you start scraping, pull snapshots via the Wayback Machine API (`waybackpy`).

### D_t — OpenRouter (primary, and the hard part)
- `https://openrouter.ai/api/v1/models` gives current pricing/metadata only, not historical volume.
- The public rankings page shows current token throughput by model; it is NOT retroactively queryable.
- For the two past events (Jan 2025 R1 release, Q2 2026 V4 episode): pull Wayback Machine snapshots of the rankings page dated as close as possible to your event windows. Expect gaps — document exactly which snapshot dates you used and their distance from the "true" event boundary.
- For anything going forward: **start a weekly cron scrape now.** This is the only way to get a clean prospective event if a new price shock happens before you submit.
- Secondary/coarse: provider-disclosed aggregate usage (OpenAI/Google/Anthropic blog posts, investor calls) — irregular cadence, but real numbers, useful as a macro-trend sanity check even if not usable for arc elasticity.

### X_t — Controls
- Ramp AI Index (public, business card-spend based adoption proxy): ramp.com/reports/ai-index — check current export options.
- Stack Overflow Developer Survey (annual) — developer population / AI-tool-usage trend, coarse.

### Z_t — Instruments
- Epoch AI compute/hardware datasets: accelerator release dates, cost-per-FLOP over time.
- Open-weight model release dates as step dummies (DeepSeek V3/R1/V4, Llama releases, Qwen, Kimi K2 — compile a release-date table manually from primary announcements, not secondary blog aggregation).

## 3. Event windows

| Event | Pre-window | Post-window | Notes |
|---|---|---|---|
| DeepSeek R1 | ~2 weeks before Jan 20 2025 | ~4-6 weeks after | Confirm exact release date from DeepSeek's own announcement, not secondary sources |
| DeepSeek V4 | ~2 weeks before late Apr 2026 | through the point OpenRouter share data stabilizes | Coincided with GPT-5.5 release same day — flag as a confound, may need to control for it explicitly |

## 4. Pipeline steps

1. Set up environment (see requirements.txt).
2. Pull and clean Epoch AI datasets -> build C_t (monthly, full history).
3. Scrape Artificial Analysis -> cross-check C_t; reconcile discrepancies, document reconciliation rule.
4. Assemble D_t: provider disclosures for macro trend; Wayback snapshots + prospective scrape for event windows.
5. Assemble X_t, Z_t.
6. Merge into a single monthly panel. Log-transform C_t, D_t.
7. Detrend/first-difference (Section 2.5.1 threat #1).
8. Run OLS log-log on detrended series -> epsilon_macro (naive).
9. Run 2SLS with Z_t as instrument for C_t -> epsilon_macro (IV).
10. Run provider-panel fixed-effects version -> epsilon (within, upper bound per Section 2.5.1 threat #3).
11. Compute arc elasticity (log-arc + midpoint) for both DeepSeek events using actual D_t token volume, not visitor/download proxies.
12. Robustness: vary input:output blend ratio (1:1 to 5:1), vary tau, placebo test on a randomly chosen non-event month.
13. Generate figures (see below).
14. Write up: record every data-pull date. These are live web sources and will have moved by the time you write Methods — cite retrieval dates, not just URLs.

## 5. Suggested figures

1. C(t) and D(t) trajectories, dual axis, full sample.
2. E(t) under the naive vs. IV vs. panel epsilon estimates, contrasted with actual reported aggregate energy (IEA data centre series) as a reality check.
3. Midpoint-attenuation curve (Proposition 4) with your two empirical arc points plotted on it.
4. Log-log scatter of D_t vs C_t with the fitted line (the actual regression, shown, not just reported).
5. Clawback curve phi(epsilon) from Proposition 6, with your estimated epsilon marked.

## 6. Tools

- Python 3.11+
- pandas, numpy — wrangling
- requests, beautifulsoup4, waybackpy — acquisition
- statsmodels — OLS
- linearmodels — panel fixed effects, 2SLS
- matplotlib — figures
- git — version control from day one; keep raw pulls and derived series in separate tracked files so the pipeline is auditable

## 7. Known weaknesses to flag in the paper itself

- D_t has no clean public retroactive source. Say this explicitly in Methods rather than letting a reviewer discover it.
- The capability threshold tau is a researcher choice, not a given. Run at least two tau values and show epsilon is stable across them, or report the sensitivity honestly if it isn't.
- Grid-capacity constraints (moratoria, interconnection queues) may bind during parts of the 2026 sample, which biases realized D_t away from the true demand curve during those windows. Consider excluding or flagging heavily-constrained months.
