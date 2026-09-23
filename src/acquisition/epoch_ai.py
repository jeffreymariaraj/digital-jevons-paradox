"""
Acquisition script for Epoch AI's public datasets (DATA_PIPELINE.md Section 2, C_t primary).

IMPORTANT — read before wiring this into a C_t transformer:

DATA_PIPELINE.md's spec for C_t assumes Epoch AI publishes, per model,
separate input price/M tokens and output price/M tokens, plus a benchmark
score, so that C_t can be built with a *configurable* blend ratio and a
*configurable* capability threshold tau. As of the retrieval dates logged
by this script, that is not what Epoch AI's public downloads contain:

1. `notable_ai_models.csv` (the bulk model-metadata export Epoch AI
   recommends for analysis) has 47 columns of compute/training/accessibility
   metadata (params, training FLOP, training cost, hardware, etc.) and
   contains NO pricing columns and NO benchmark score columns at all.

2. The only place Epoch AI publishes token price tied to benchmark
   performance is the "LLM inference price trends" data insight
   (https://epoch.ai/data-insights/llm-inference-price-trends). Its
   underlying chart data (fetched by this script as
   lowest_price_models_data.csv / other_models_data.csv) has real
   limitations documented in that page's own methodology section:
     - Only ~36 unique model/price observations total, across 6
       benchmarks (GPQA Diamond, MMLU, MATH-500, MATH level 5, HumanEval,
       Chatbot Arena Elo).
     - Price is a single pre-blended "USD per 1M Tokens" figure computed
       at a FIXED 3:1 input:output weighting (Artificial Analysis's
       methodology, which Epoch adopted) — there is no separate input/
       output field in this file to re-blend at a different ratio.
     - Most observations (27 of 36) are sourced from Artificial Analysis,
       not measured by Epoch directly; Epoch contributed prices only for
       GPT-3, GPT-3.5, and Llama 2 models that Artificial Analysis lacked.
     - Reasoning models are explicitly excluded from this dataset by
       Epoch's stated methodology. DeepSeek-R1 does not appear in either
       file for this reason — this directly affects the R1 event study.

This script only lands the raw files and documents what's actually in
them (see data/raw/epoch_ai/PROVENANCE.md, written alongside the data on
each run). It does NOT implement the configurable-blend-ratio C_t
transformer DATA_PIPELINE.md describes, because building it from this
data would mean either fabricating an input/output split that doesn't
exist, or silently presenting Epoch's fixed 3:1 ratio as if it were the
configurable one the paper's sensitivity analysis (step 12) needs.
"""

import csv
from datetime import datetime, timezone
from pathlib import Path

import requests

from src.common.logging_config import get_logger, log_retrieval

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw" / "epoch_ai"

NOTABLE_MODELS_URL = "https://epoch.ai/data/notable_ai_models.csv"
INFERENCE_PRICE_TREND_PAGE = "https://epoch.ai/data-insights/llm-inference-price-trends"
INFERENCE_PRICE_CHART_URLS = {
    "lowest_price_models_data.csv": (
        "https://epoch.ai/data/charts/llm-inference-price-trends/lowest_price_models_data.csv"
    ),
    "other_models_data.csv": (
        "https://epoch.ai/data/charts/llm-inference-price-trends/other_models_data.csv"
    ),
}

USER_AGENT = "Mozilla/5.0 (FAccT paper research pipeline; contact: playstationblr4@gmail.com)"
REQUEST_TIMEOUT_S = 30


def _today_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def _fetch(url: str, logger) -> requests.Response:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT_S)
    resp.raise_for_status()
    return resp


def fetch_notable_ai_models(logger) -> Path:
    """Land Epoch AI's Notable AI Models CSV (model metadata; no pricing/benchmark columns)."""
    resp = _fetch(NOTABLE_MODELS_URL, logger)
    out_path = RAW_DIR / f"notable_ai_models_{_today_stamp()}.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(resp.content)
    log_retrieval(
        logger,
        source="Epoch AI - Notable AI Models",
        url=NOTABLE_MODELS_URL,
        note=f"saved to {out_path.relative_to(RAW_DIR.parent.parent.parent)}, "
        f"{len(resp.content) / 1024:.1f} KiB",
    )
    return out_path


def fetch_inference_price_trend_data(logger) -> dict[str, Path]:
    """Land the two chart CSVs backing Epoch AI's LLM inference price trends page.

    These are not listed on epoch.ai/data as a generic bulk download — they are
    the specific chart-data files embedded in the data-insight page above.
    Returns a dict keyed by the original filename (as used in
    INFERENCE_PRICE_CHART_URLS), mapping to the saved, date-stamped path.
    """
    saved = {}
    for filename, url in INFERENCE_PRICE_CHART_URLS.items():
        resp = _fetch(url, logger)
        stem, ext = filename.rsplit(".", 1)
        out_path = RAW_DIR / f"{stem}_{_today_stamp()}.{ext}"
        out_path.write_bytes(resp.content)
        log_retrieval(
            logger,
            source="Epoch AI - LLM inference price trends (chart data)",
            url=url,
            note=f"backing page={INFERENCE_PRICE_TREND_PAGE}, "
            f"saved to {out_path.relative_to(RAW_DIR.parent.parent.parent)}, "
            f"{len(resp.content) / 1024:.1f} KiB",
        )
        saved[filename] = out_path
    return saved


def _count_rows(path: Path) -> int:
    with open(path, newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.reader(f)) - 1  # exclude header


def write_provenance_note(logger, notable_path: Path, chart_paths: dict[str, Path]) -> Path:
    """Write a human-readable provenance note next to the raw files.

    This is what should get cited (with retrieval date) in the paper's
    Methods/reproducibility section — not just the source URLs, since the
    URLs alone don't convey the schema gaps documented in this module's
    docstring.
    """
    retrieved_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Epoch AI raw data provenance",
        "",
        f"Retrieved: {retrieved_at}",
        "",
        f"## {notable_path.name}",
        f"- Source: {NOTABLE_MODELS_URL}",
        f"- Rows: {_count_rows(notable_path)} (excl. header)",
        "- Contains model metadata (compute, training cost, accessibility, etc.).",
        "- Does NOT contain pricing or benchmark-score columns.",
        "",
    ]
    for filename, p in chart_paths.items():
        lines += [
            f"## {p.name}",
            f"- Source: {INFERENCE_PRICE_CHART_URLS[filename]}",
            f"- Backing page: {INFERENCE_PRICE_TREND_PAGE}",
            f"- Rows: {_count_rows(p)} (excl. header)",
            "",
        ]
    lines += [
        "## Known limitations (see src/acquisition/epoch_ai.py module docstring for full detail)",
        "- Price is pre-blended at a fixed 3:1 input:output ratio, not separable.",
        "- Reasoning models (incl. DeepSeek-R1) are excluded by Epoch's own methodology.",
        "- Most observations are sourced from Artificial Analysis, not Epoch directly.",
        "- Only ~36 unique model/price observations total, across 6 benchmarks.",
    ]
    out_path = RAW_DIR / f"PROVENANCE_{_today_stamp()}.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Wrote provenance note to %s", out_path)
    return out_path


def main() -> None:
    logger = get_logger("epoch_ai_acquisition")
    notable_path = fetch_notable_ai_models(logger)
    chart_paths = fetch_inference_price_trend_data(logger)
    write_provenance_note(logger, notable_path, chart_paths)
    logger.info(
        "Done. NOTE: no C_t transformer has been run — see module docstring; "
        "the blend-ratio/tau construction DATA_PIPELINE.md describes is blocked "
        "on a source with separable input/output pricing."
    )


if __name__ == "__main__":
    main()
