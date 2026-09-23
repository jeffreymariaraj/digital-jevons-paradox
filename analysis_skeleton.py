"""
Analysis skeleton for the Digital Jevons Paradox paper.
Wires up the Section 2 formulas. Point the loader functions at your
assembled dataframes once the pipeline in DATA_PIPELINE.md is run.

Expected input schema (pandas DataFrame, monthly panel):
    date        : datetime
    C           : float, price per M tokens at fixed capability threshold
    D           : float, aggregate token volume (or a chosen proxy)
    provider    : str, optional — only needed for the panel/FE spec
    X_...       : float, control columns (developer pop, adoption index, etc.)
    Z_...       : float, instrument columns (cost-per-FLOP, release dummies)
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS
from linearmodels.panel import PanelOLS


# ---------------------------------------------------------------------------
# 1. Macro log-log regression (naive OLS) — Section 2.5.1, baseline spec
# ---------------------------------------------------------------------------
def run_macro_ols(df: pd.DataFrame, control_cols: list[str]) -> sm.regression.linear_model.RegressionResultsWrapper:
    """
    ln D_t = ln k + eps_macro * ln C_t + delta' X_t + u_t

    NOTE: this is the naive spec Section 2.5.1 warns is close to guaranteed
    to find eps < -1 due to trend confounding. Report it, but do not treat
    it as the headline number — pair with run_macro_iv() and
    run_detrended_ols() below.
    """
    y = np.log(df["D"])
    X = pd.DataFrame({"ln_C": np.log(df["C"])})
    for c in control_cols:
        X[c] = df[c]
    X = sm.add_constant(X)
    model = sm.OLS(y, X, missing="drop")
    return model.fit(cov_type="HC1")


def run_detrended_ols(df: pd.DataFrame, control_cols: list[str]) -> sm.regression.linear_model.RegressionResultsWrapper:
    """
    First-differenced version: removes the shared time trend that biases
    the naive spec. This is the minimum bar before eps_macro is reportable.
    """
    d = df.sort_values("date").copy()
    d["d_ln_D"] = np.log(d["D"]).diff()
    d["d_ln_C"] = np.log(d["C"]).diff()
    X = pd.DataFrame({"d_ln_C": d["d_ln_C"]})
    for c in control_cols:
        X[f"d_{c}"] = d[c].diff()
    X = sm.add_constant(X)
    model = sm.OLS(d["d_ln_D"], X, missing="drop")
    return model.fit(cov_type="HC1")


# ---------------------------------------------------------------------------
# 2. IV / 2SLS — instrument ln_C with hardware cost-per-FLOP or release dummy
# ---------------------------------------------------------------------------
def run_macro_iv(df: pd.DataFrame, control_cols: list[str], instrument_cols: list[str]):
    """
    Instruments ln C_t with supply-side shifters (Z_t) plausibly orthogonal
    to demand shocks — accelerator generation cost-per-FLOP, open-weight
    release dummies. See Section 2.5.1, identification threat #2.
    """
    d = df.dropna(subset=["D", "C"] + control_cols + instrument_cols).copy()
    dependent = np.log(d["D"])
    exog = sm.add_constant(d[control_cols]) if control_cols else pd.DataFrame({"const": np.ones(len(d))})
    endog = np.log(d["C"])
    instruments = d[instrument_cols]
    model = IV2SLS(dependent, exog, endog, instruments)
    return model.fit(cov_type="robust")


# ---------------------------------------------------------------------------
# 3. Provider panel with fixed effects — Section 2.5.1, threat #3
#    (substitution elasticity; report as upper bound on |eps_macro|, not headline)
# ---------------------------------------------------------------------------
def run_panel_fe(df: pd.DataFrame, control_cols: list[str]):
    """
    Requires a 'provider' column and a MultiIndex of (provider, date).
    ln D_it = mu_i + lambda_t + eps * ln C_it + u_it
    """
    d = df.set_index(["provider", "date"]).copy()
    d["ln_D"] = np.log(d["D"])
    d["ln_C"] = np.log(d["C"])
    exog_cols = ["ln_C"] + control_cols
    exog = sm.add_constant(d[exog_cols])
    model = PanelOLS(d["ln_D"], exog, entity_effects=True, time_effects=True)
    return model.fit(cov_type="clustered", cluster_entity=True)


# ---------------------------------------------------------------------------
# 4. Arc elasticity for discrete shocks — Section 2.5.2 / 3.4
# ---------------------------------------------------------------------------
def arc_elasticity_midpoint(C1: float, C2: float, D1: float, D2: float) -> float:
    """Proposition 4's midpoint formula. Biased toward -1, conservative for
    classifying backfire but compresses magnitude — see Section 2.5.2."""
    d_pct = (D2 - D1) / ((D1 + D2) / 2)
    c_pct = (C2 - C1) / ((C1 + C2) / 2)
    return d_pct / c_pct


def arc_elasticity_log(C1: float, C2: float, D1: float, D2: float) -> float:
    """Log-arc elasticity: exact under constant elasticity, comparable
    directly to the regression coefficient eps_macro."""
    return np.log(D2 / D1) / np.log(C2 / C1)


def rebound_multiplier(gamma: float, epsilon: float) -> float:
    """Proposition 2's R(gamma, epsilon). gamma = C2/C1, in (0,1)."""
    return (gamma ** (1 + epsilon) - gamma) / (1 - gamma)


def clawback_fraction(epsilon: float, tau_p: float = 3.5, tau_e: float = 3.5) -> float:
    """Proposition 6, general form: phi = 1 - tau_p / (|eps| * tau_e).
    NOTE: corrects the sign error flagged in the Section 4 revision notes —
    verify this derivation yourself before using it in the paper."""
    return 1 - tau_p / (abs(epsilon) * tau_e)


# ---------------------------------------------------------------------------
# 5. Robustness helpers
# ---------------------------------------------------------------------------
def blend_price(input_price: float, output_price: float, input_weight: float = 0.75) -> float:
    """Blended C for a given input:output token-count ratio.
    input_weight=0.75 corresponds to a 3:1 input:output ratio."""
    return input_weight * input_price + (1 - input_weight) * output_price


def sensitivity_over_blend_ratios(input_price: float, output_price: float,
                                   ratios: list[float] = [0.5, 0.6, 0.75, 0.8]) -> dict[float, float]:
    """Sweep the input:output blend assumption — report how much C1/C2
    (and hence gamma, and hence arc elasticity) moves with this choice."""
    return {r: blend_price(input_price, output_price, r) for r in ratios}


if __name__ == "__main__":
    # Example wiring once your dataframe is assembled:
    # df = pd.read_parquet("data/monthly_panel.parquet")
    # controls = ["X_ramp_index", "X_dev_population"]
    # instruments = ["Z_cost_per_flop"]
    #
    # naive = run_macro_ols(df, controls)
    # detrended = run_detrended_ols(df, controls)
    # iv = run_macro_iv(df, controls, instruments)
    # print(naive.summary())
    # print(detrended.summary())
    # print(iv.summary)
    #
    # DeepSeek R1 event (example placeholders — replace with real pulled values):
    # eps_log = arc_elasticity_log(C1=26.25, C2=0.96, D1=..., D2=...)
    # eps_mid = arc_elasticity_midpoint(C1=26.25, C2=0.96, D1=..., D2=...)
    pass
