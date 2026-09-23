# Densing Law / Digital Jevons Paradox — data pipeline

Empirical pipeline for the FAccT submission. Spec lives in `DATA_PIPELINE.md`;
regression/arc-elasticity functions live in `analysis_skeleton.py`. This repo
implements acquisition and testing around that spec — it does not redefine it.

## Structure

- `data/raw/` — landed pulls, as close to source format as practical (tracked
  in git per DATA_PIPELINE.md Section 6, so the pipeline stays auditable).
- `data/processed/` — derived series (e.g. the constructed `C_t`/`D_t` panel).
- `src/acquisition/` — scripts that pull from Epoch AI, Wayback Machine, and
  OpenRouter live.
- `src/analysis/` — reserved for analysis code split out of
  `analysis_skeleton.py` once real data exists; empty until then.
- `src/common/` — shared utilities (currently: `logging_config.py`).
- `notebooks/` — exploration; not treated as a source of truth for results.
- `tests/` — unit tests, including synthetic-data tests against
  `analysis_skeleton.py`.
- `logs/` — one timestamped log file per acquisition run (gitignored; the
  `RETRIEVED ...` lines each run emits are what to cite in Methods for
  retrieval dates — copy them out rather than committing raw logs).

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Status

Environment and structure only — no data pulled yet. See conversation/PR
history for the order acquisition scripts were added in.
