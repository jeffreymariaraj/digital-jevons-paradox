# Epoch AI raw data provenance

Retrieved: 2026-09-23T09:01:11Z

## notable_ai_models_20260923.csv
- Source: https://epoch.ai/data/notable_ai_models.csv
- Rows: 1072 (excl. header)
- Contains model metadata (compute, training cost, accessibility, etc.).
- Does NOT contain pricing or benchmark-score columns.

## lowest_price_models_data_20260923.csv
- Source: https://epoch.ai/data/charts/llm-inference-price-trends/lowest_price_models_data.csv
- Backing page: https://epoch.ai/data-insights/llm-inference-price-trends
- Rows: 119 (excl. header)

## other_models_data_20260923.csv
- Source: https://epoch.ai/data/charts/llm-inference-price-trends/other_models_data.csv
- Backing page: https://epoch.ai/data-insights/llm-inference-price-trends
- Rows: 371 (excl. header)

## Known limitations (see src/acquisition/epoch_ai.py module docstring for full detail)
- Price is pre-blended at a fixed 3:1 input:output ratio, not separable.
- Reasoning models (incl. DeepSeek-R1) are excluded by Epoch's own methodology.
- Most observations are sourced from Artificial Analysis, not Epoch directly.
- Only ~36 unique model/price observations total, across 6 benchmarks.