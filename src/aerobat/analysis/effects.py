"""Randomized-block analysis of hypothesized behavioral effects."""

from __future__ import annotations

import hashlib
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence

from .helpers import (
    _coerce_float,
    _fmt_bf,
    _fmt_idx,
    _mean_score_per_condition,
    _one_hot,
    _round_3,
    _rows_by_hypothesis,
    _rows_by_block,
)
from .score_rows import behavior_evidence_class_score_rows, behavior_score_rows


@dataclass(frozen=True)
class MonotoneAnalysisOptions:
    """Numerical options for the paper's Bayesian monotone-increment model."""

    effect_bf10: float = 3.0
    no_effect_bf10: float = 1 / 3
    direction_probability: float = 0.95
    tau_near_zero: float = 0.1
    prior_scale: float = math.sqrt(2) / 2
    increment_samples: int = 512
    prior_grid_points: int = 257
    tau_permutations: int = 5_000


def analyze_hypothesis_effect(
    rows: Sequence[Mapping[str, Any]],
    options: MonotoneAnalysisOptions = MonotoneAnalysisOptions(),
) -> Dict[str, Any]:
    """Analyze one hypothesis across its matched-configuration blocks."""
    return {
        "n": len(rows),
        **_analyze_hypothesis_effect(
            rows,
            effect_bf_threshold=options.effect_bf10,
            no_effect_bf_threshold=options.no_effect_bf10,
            tau_near_zero_threshold=options.tau_near_zero,
            monotone_prior_scale=options.prior_scale,
            monotone_increment_samples=options.increment_samples,
            monotone_prior_grid_points=options.prior_grid_points,
            monotone_direction_probability_threshold=options.direction_probability,
            tau_permutations=options.tau_permutations,
        ),
    }


def _block_stratified_kendall_tau_from_pairs(
    pairs_by_block: Mapping[str, Sequence[tuple[float, float]]],
) -> Dict[str, Any]:
    concordant = 0
    discordant = 0
    x_ties = 0
    y_ties = 0
    both_ties = 0
    pair_counts_by_block: Dict[str, Dict[str, int]] = {}

    for block_id, pairs in pairs_by_block.items():
        if len(pairs) < 2:
            continue
        block_counts = {
            "concordant": 0,
            "discordant": 0,
            "x_ties": 0,
            "y_ties": 0,
            "both_ties": 0,
            "pairs": 0,
        }

        for left_index in range(len(pairs)):
            for right_index in range(left_index + 1, len(pairs)):
                x_left, y_left = pairs[left_index]
                x_right, y_right = pairs[right_index]
                x_diff = x_left - x_right
                y_diff = y_left - y_right
                block_counts["pairs"] += 1
                if x_diff == 0 and y_diff == 0:
                    both_ties += 1
                    block_counts["both_ties"] += 1
                elif x_diff == 0:
                    x_ties += 1
                    block_counts["x_ties"] += 1
                elif y_diff == 0:
                    y_ties += 1
                    block_counts["y_ties"] += 1
                elif x_diff * y_diff > 0:
                    concordant += 1
                    block_counts["concordant"] += 1
                else:
                    discordant += 1
                    block_counts["discordant"] += 1
        pair_counts_by_block[block_id] = block_counts

    denominator = math.sqrt(
        (concordant + discordant + x_ties)
        * (concordant + discordant + y_ties)
    )
    tau = (concordant - discordant) / denominator if denominator > 0 else None

    return {
        "tau": tau,
        "concordant": concordant,
        "discordant": discordant,
        "x_ties": x_ties,
        "y_ties": y_ties,
        "both_ties": both_ties,
        "pairs": concordant + discordant + x_ties + y_ties + both_ties,
        "pair_counts_by_block": pair_counts_by_block,
        "blocks": len(pair_counts_by_block),
        # Legacy artifact value; the public API calls this block-stratified Kendall's tau.
        "method": "Group-stratified Kendall tau from within-group pair counts",
    }


def _block_stratified_kendall_tau(
    rows: Sequence[Mapping[str, Any]],
    *,
    permutations: int = 5000,
) -> Dict[str, Any]:
    pairs_by_block: Dict[str, List[tuple[float, float]]] = {}
    for block_rows in _rows_by_block(rows).values():
        pairs = [
            (x, y)
            for row in sorted(
                block_rows,
                key=lambda row: (
                    _coerce_float(row.get("causal_rank"))
                    if _coerce_float(row.get("causal_rank")) is not None
                    else 10**9
                ),
            )
            if (x := _coerce_float(row.get("causal_rank"))) is not None
            and (y := _coerce_float(row.get("behavior_eval_mean_score"))) is not None
        ]
        if len(pairs) < 2:
            continue
        block_id = str(block_rows[0]["group_id"])
        pairs_by_block[block_id] = pairs

    observed = _block_stratified_kendall_tau_from_pairs(pairs_by_block)
    observed_tau = observed.get("tau")
    if not isinstance(observed_tau, (int, float)) or permutations <= 0:
        return {
            **observed,
            "p_tau": None,
            "permutations": 0,
        }

    rng = random.Random(f"block-stratified-tau:{pairs_by_block}")
    exceedances = 0
    for _ in range(permutations):
        permuted_pairs_by_block = {}
        for block_id, pairs in pairs_by_block.items():
            x_values = [x for x, _ in pairs]
            y_values = [y for _, y in pairs]
            rng.shuffle(x_values)
            permuted_pairs_by_block[block_id] = list(zip(x_values, y_values))
        permuted_tau = _block_stratified_kendall_tau_from_pairs(permuted_pairs_by_block).get("tau")
        if isinstance(permuted_tau, (int, float)) and abs(permuted_tau) >= abs(observed_tau):
            exceedances += 1

    return {
        **observed,
        "p_tau": (1 + exceedances) / (permutations + 1),
        "permutations": permutations,
    }


def _clean_behavior_rows(rows: Sequence[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
    return [
        row
        for row in rows
        if _coerce_float(row.get("causal_rank")) is not None
        and _coerce_float(row.get("behavior_eval_mean_score")) is not None
    ]


def _analysis_seed(rows: Sequence[Mapping[str, Any]], label: str) -> int:
    payload = [
        (
            row["group_id"],
            _coerce_float(row.get("causal_rank")),
            _coerce_float(row.get("behavior_eval_mean_score")),
        )
        for row in rows
    ]
    digest = hashlib.sha256(repr((label, payload)).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def _monotone_increment_draws(
    *,
    level_count: int,
    samples: int,
    seed: int,
) -> Any:
    import numpy as np

    increment_count = level_count - 1
    if increment_count <= 0:
        return np.empty((0, 0), dtype=float)
    if increment_count == 1:
        return np.ones((1, 1), dtype=float)

    rng = np.random.default_rng(seed)
    draw_count = max(1, int(samples))
    return rng.dirichlet(np.ones(increment_count), size=draw_count)


def _block_residuals(values: Any, block_matrix: Any) -> Any:
    import numpy as np

    coefficients, *_ = np.linalg.lstsq(block_matrix, values, rcond=None)
    return values - block_matrix @ coefficients


def _monotone_prior_scale_grid(*, prior_scale: float, points: int) -> Any:
    """Equal-prior-mass grid for the Cauchy scale mixture.

    ``d ~ Cauchy(0, r)`` is written as ``d | g ~ Normal(0, g)`` with
    ``g ~ InverseGamma(1/2, r^2/2)``, i.e. ``g = r^2 / X`` for ``X ~ ChiSquare(1)``.
    Gridding the mixing distribution on its own CDF gives every node equal prior
    mass, so integrating over the prior is a plain average over the grid.
    """

    import numpy as np
    from scipy import stats

    quantiles = (np.arange(points, dtype=float) + 0.5) / points
    return prior_scale**2 / stats.chi2.ppf(quantiles, 1)


def _log10_bf10_mcse(log_bf_values: Any, log_bf10: float) -> Optional[float]:
    """Monte Carlo standard error of ``log10 BF10`` from the per-increment Bayes factors.

    ``BF10`` is the sample mean of ``B_k = exp(log_bf_values[k])`` over the Dirichlet
    draws, so its standard error is ``sd(B_k) / sqrt(K)`` and first-order propagation carries
    that to ``log10 BF10`` by dividing through ``BF10 * ln 10``. Both moments are taken
    in log space because ``B_k`` routinely overflows. With a single increment shape
    (``J = 2``) the expectation over the shape prior is exact, so the error is zero.
    """

    import numpy as np
    from scipy.special import logsumexp

    draw_count = int(len(log_bf_values))
    if draw_count < 2:
        return 0.0

    log_second_moment = float(logsumexp(2 * log_bf_values) - math.log(draw_count))
    # Jensen guarantees log E[B^2] >= 2 log E[B]; the ratio is 1 only for constant B_k.
    log_ratio = min(2 * log_bf10 - log_second_moment, 0.0)
    if log_ratio >= -1e-15:
        return 0.0
    log_variance = log_second_moment + math.log1p(-math.exp(log_ratio))
    log_variance += math.log(draw_count / (draw_count - 1))  # unbiased sample variance
    log_mcse = 0.5 * log_variance - log_bf10 - 0.5 * math.log(draw_count)
    # Left unrounded, like the neighbouring bf10/bf01 fields: the error spans orders of
    # magnitude across hypotheses and three decimals would floor most of it to zero.
    return float(math.exp(log_mcse) / math.log(10))


def _monotone_unavailable(note: str, **extra: Any) -> Dict[str, Any]:
    monotone_analysis = {
        "bf10": None,
        "bf01": None,
        "log10_bf10_mcse": None,
        "direction": "direction_unresolved",
        "p_beta_gt_0": None,
        "p_beta_lt_0": None,
        "note": note,
        **extra,
    }
    return {
        "prior": None,
        "monotone_analysis": monotone_analysis,
        "effect_size": {
            "beta": None,
            "beta_ci_95": None,
            "Delta": None,
            "Delta_ci_95": None,
            "residual_sd": None,
            "method": None,
        },
    }


def _mixture_t_quantiles(
    *,
    locations: Any,
    scales: Any,
    weights: Any,
    df: int,
    probabilities: Sequence[float],
) -> List[float]:
    """Quantiles of a weighted mixture of Student-t densities, found by bisection."""

    import numpy as np
    from scipy import stats

    def cdf(value: float) -> float:
        return float(np.sum(weights * stats.t.cdf((value - locations) / scales, df)))

    spread = float(np.max(scales)) * float(stats.t.ppf(0.9999, df))
    low = float(np.min(locations)) - spread
    high = float(np.max(locations)) + spread

    out = []
    for probability in probabilities:
        left, right = low, high
        for _ in range(200):
            middle = (left + right) / 2
            if cdf(middle) < probability:
                left = middle
            else:
                right = middle
            if right - left < 1e-9 * max(1.0, abs(middle)):
                break
        out.append((left + right) / 2)
    return out


def _fit_bayesian_monotone_increment_model(
    rows: Sequence[Mapping[str, Any]],
    *,
    prior_scale: float = math.sqrt(2) / 2,
    increment_samples: int = 512,
    prior_grid_points: int = 257,
    direction_probability_threshold: float = 0.95,
) -> Dict[str, Any]:
    """Bayesian monotone-increment analysis of a blocked ordinal-X design.

    Fits ``y_bj = mu + w_b + beta * m_j + eps`` where ``m_1 = 0``, ``m_J = 1`` and
    the adjacent increments carry a ``Dirichlet(1)`` prior (Buerkner & Charpentier,
    2020), so ``beta`` is the endpoint contrast and ``M1`` is monotone by
    construction in either direction.

    The block effects are removed by orthogonal projection, which under flat priors
    on ``(mu, w)`` leaves the Bayes factor unchanged. The error scale carries a
    Jeffreys prior and is integrated out analytically: writing the endpoint prior
    ``Delta = beta / sigma ~ Cauchy(0, r)`` as a normal scale mixture makes the marginal
    likelihood available in closed form for each mixing value ``g``, and the
    posterior of ``beta`` a weighted mixture of Student-t densities.
    """

    import numpy as np
    from scipy.special import gammaln, logsumexp

    if prior_scale <= 0:
        raise ValueError("prior_scale must be positive")
    if prior_grid_points < 17:
        raise ValueError("prior_grid_points must be at least 17")
    if direction_probability_threshold <= 0.5 or direction_probability_threshold >= 1:
        raise ValueError("direction_probability_threshold must be between 0.5 and 1")

    clean_rows = _clean_behavior_rows(rows)
    n = len(clean_rows)
    if n < 4:
        return _monotone_unavailable("Fewer than four usable observations.")

    groups = [
        row["group_id"]
        for row in clean_rows
    ]
    ranks = [_coerce_float(row.get("causal_rank")) for row in clean_rows]
    y = np.array(
        [_coerce_float(row.get("behavior_eval_mean_score")) for row in clean_rows],
        dtype=float,
    )
    levels = sorted(set(ranks))
    level_count = len(levels)
    if level_count < 2:
        return _monotone_unavailable("Only one level of X is present.")

    _, group_columns = _one_hot(groups, drop_first=True)
    block_matrix = np.array([[1.0] + block for block in group_columns], dtype=float)
    block_rank = int(np.linalg.matrix_rank(block_matrix))
    df = n - block_rank
    if df < 3:
        return _monotone_unavailable(
            f"Only {df} residual degrees of freedom after the matched-group effects."
        )

    y_residual = _block_residuals(y, block_matrix)
    null_sse = float(np.sum(y_residual**2))
    if null_sse <= 1e-12:
        # The matched-group means reproduce the scores exactly, so the model carries
        # no residual variation and the Bayes factor is undefined rather than decisive.
        return _monotone_unavailable(
            "Behavior scores are constant within every matched group; "
            "the monotone model is degenerate."
        )

    level_index_by_rank = {level: index for index, level in enumerate(levels)}
    row_level_indices = np.array([level_index_by_rank[rank] for rank in ranks], dtype=int)

    g_grid = _monotone_prior_scale_grid(
        prior_scale=prior_scale,
        points=prior_grid_points,
    )
    increments = _monotone_increment_draws(
        level_count=level_count,
        samples=increment_samples,
        seed=_analysis_seed(clean_rows, "monotone-increment-dirichlet"),
    )

    log_bf_by_increment = []
    valid_increments = []
    component_log_bf = []
    component_location = []
    component_scale = []
    component_residual_sd = []

    for increment in increments:
        m_by_level = np.concatenate([[0.0], np.cumsum(increment)])
        x_residual = _block_residuals(m_by_level[row_level_indices], block_matrix)
        x_sum_squares = float(np.sum(x_residual**2))
        if x_sum_squares <= 1e-12:
            continue
        cross_product = float(y_residual @ x_residual)

        # beta | sigma, g ~ Normal(0, g sigma^2) and p(sigma) ∝ 1/sigma give, for each g,
        # a closed-form Bayes factor and a Student-t posterior for beta.
        precision = x_sum_squares + 1 / g_grid
        location = cross_product / precision
        model_sse = np.maximum(null_sse - cross_product * location, 1e-300)
        log_bf_by_g = -0.5 * np.log1p(g_grid * x_sum_squares) - (df / 2) * np.log(
            model_sse / null_sse
        )

        log_bf_by_increment.append(
            float(logsumexp(log_bf_by_g) - math.log(len(g_grid)))
        )
        valid_increments.append(increment)
        component_log_bf.append(log_bf_by_g)
        component_location.append(location)
        component_scale.append(np.sqrt(model_sse / (precision * df)))
        # E[sigma | y, g] under the monotone model, from sigma^2 ~ InvGamma(df/2, sse/2).
        component_residual_sd.append(
            np.sqrt(model_sse / 2) * math.exp(gammaln((df - 1) / 2) - gammaln(df / 2))
        )

    if not log_bf_by_increment:
        return _monotone_unavailable(
            "The monotone regressor is collinear with the matched-group effects."
        )

    log_bf_values = np.array(log_bf_by_increment, dtype=float)
    log_bf10 = float(logsumexp(log_bf_values) - math.log(len(log_bf_values)))
    bf10 = math.exp(min(log_bf10, 700))
    bf01 = 1 / bf10 if bf10 > 0 else float("inf")
    log10_bf10_mcse = _log10_bf10_mcse(log_bf_values, log_bf10)

    # Posterior over (increment shape, mixing value), weighted by marginal likelihood.
    log_weights = np.concatenate(component_log_bf)
    log_weights -= float(logsumexp(log_weights))
    weights = np.exp(log_weights)
    locations = np.concatenate(component_location)
    scales = np.concatenate(component_scale)
    residual_sds = np.concatenate(component_residual_sd)

    beta_mean = float(np.sum(weights * locations))
    residual_sd = float(np.sum(weights * residual_sds))
    beta_ci = _mixture_t_quantiles(
        locations=locations,
        scales=scales,
        weights=weights,
        df=df,
        probabilities=[0.025, 0.975],
    )

    from scipy import stats

    p_beta_gt_0 = float(np.sum(weights * stats.t.cdf(locations / scales, df)))
    p_beta_lt_0 = 1 - p_beta_gt_0

    bf_weights = np.exp(log_bf_values - float(logsumexp(log_bf_values)))
    increment_mean = np.sum(np.array(valid_increments) * bf_weights[:, None], axis=0)
    m_mean = np.concatenate([[0.0], np.cumsum(increment_mean)])

    if p_beta_gt_0 > direction_probability_threshold:
        direction = "positive"
    elif p_beta_lt_0 > direction_probability_threshold:
        direction = "negative"
    else:
        direction = "direction_unresolved"

    method = (
        "Bayesian monotone-increment model with Dirichlet(1) adjacent increments; "
        "block effects residualized; error scale integrated under a Jeffreys prior; "
        "beta standardized by the posterior mean residual SD of the monotone model"
    )
    return {
        "prior": f"Cauchy(0, {prior_scale:g}) on Delta=beta/sigma",
        "monotone_analysis": {
            "bf10": float(bf10),
            "bf01": float(bf01),
            "log10_bf10_mcse": log10_bf10_mcse,
            "direction": direction,
            "p_beta_gt_0": _round_3(p_beta_gt_0),
            "p_beta_lt_0": _round_3(p_beta_lt_0),
            "df": df,
            "posterior_mean_increment": [_round_3(value) for value in increment_mean],
            "posterior_mean_m_by_rank": {
                str(_round_3(level)): _round_3(value)
                for level, value in zip(levels, m_mean)
            },
            "increment_samples": len(valid_increments),
            "prior_grid_points": int(len(g_grid)),
            "direction_probability_threshold": direction_probability_threshold,
        },
        "effect_size": {
            "beta": _round_3(beta_mean),
            "beta_ci_95": [_round_3(value) for value in beta_ci],
            "Delta": _round_3(beta_mean / residual_sd) if residual_sd > 0 else None,
            "Delta_ci_95": (
                [_round_3(value / residual_sd) for value in beta_ci] if residual_sd > 0 else None
            ),
            "residual_sd": _round_3(residual_sd),
            "method": method,
        },
    }


def _analyze_hypothesis_effect(
    rows: Sequence[Mapping[str, Any]],
    *,
    effect_bf_threshold: float = 3.0,
    no_effect_bf_threshold: float = 1 / 3,
    tau_near_zero_threshold: float = 0.1,
    monotone_prior_scale: float = math.sqrt(2) / 2,
    monotone_increment_samples: int = 512,
    monotone_prior_grid_points: int = 257,
    monotone_direction_probability_threshold: float = 0.95,
    tau_permutations: int = 5000,
) -> Dict[str, Any]:
    if no_effect_bf_threshold >= effect_bf_threshold:
        raise ValueError("no_effect_bf_threshold must be below effect_bf_threshold")
    if tau_near_zero_threshold < 0:
        raise ValueError("tau_near_zero_threshold must not be negative")

    tau = _block_stratified_kendall_tau(rows, permutations=tau_permutations)
    analysis = _fit_bayesian_monotone_increment_model(
        rows,
        prior_scale=monotone_prior_scale,
        increment_samples=monotone_increment_samples,
        prior_grid_points=monotone_prior_grid_points,
        direction_probability_threshold=monotone_direction_probability_threshold,
    )
    monotone = analysis["monotone_analysis"]
    effect_size = analysis["effect_size"]
    prior = analysis["prior"]
    bf10 = monotone.get("bf10")

    if not isinstance(bf10, (int, float)):
        effect_class = "inconclusive"
        rationale = (
            f"BF10 is unavailable: {monotone.get('note') or 'no monotone model was fitted'}"
        )
    elif bf10 < no_effect_bf_threshold:
        effect_class = "no_effect"
        rationale = (
            f"BF10={_fmt_bf(bf10)} is below the no-effect threshold "
            f"{no_effect_bf_threshold:g}."
        )
    elif bf10 <= effect_bf_threshold:
        effect_class = "inconclusive"
        rationale = (
            f"BF10={_fmt_bf(bf10)} is between the no-effect threshold "
            f"{no_effect_bf_threshold:g} and effect threshold {effect_bf_threshold:g}."
        )
    else:
        direction_class = monotone.get("direction")
        if direction_class in {"positive", "negative"}:
            effect_class = direction_class
            probability_key = (
                "p_beta_gt_0" if direction_class == "positive" else "p_beta_lt_0"
            )
            rationale = (
                f"BF10={_fmt_bf(bf10)} supports a monotone effect; "
                f"P(beta {'>' if direction_class == 'positive' else '<'} 0)="
                f"{_fmt_idx(monotone.get(probability_key))} supports a {direction_class} effect."
            )
        else:
            effect_class = "direction_unresolved"
            rationale = (
                f"BF10={_fmt_bf(bf10)} supports a monotone effect, but "
                f"P(beta > 0)={_fmt_idx(monotone.get('p_beta_gt_0'))} and "
                f"P(beta < 0)={_fmt_idx(monotone.get('p_beta_lt_0'))} do not clear "
                f"the {monotone_direction_probability_threshold:g} direction threshold."
            )

    tau_value = _coerce_float(tau.get("tau"))
    return {
        "effect_class": effect_class,
        "rationale": rationale,
        "prior": prior,
        "monotone_analysis": monotone,
        "effect_size": effect_size,
        "rank_correlation": {
            "tau": _round_3(tau_value),
            "p_tau": _round_3(tau.get("p_tau")),
            "permutations": tau.get("permutations", 0),
            "blocks": tau.get("blocks", 0),
            "near_zero": (abs(tau_value) < tau_near_zero_threshold) if tau_value is not None else None,
            "near_zero_threshold": tau_near_zero_threshold,
            "method": tau.get("method"),
        },
        "score_per_condition": _mean_score_per_condition(rows),
        "thresholds": {
            "effect_bf10": effect_bf_threshold,
            "no_effect_bf10": no_effect_bf_threshold,
            "monotone_direction_probability": monotone_direction_probability_threshold,
            "tau_near_zero": tau_near_zero_threshold,
        },
    }


def hypothesis_effect_rows(
    blind_reviews_by_id: Mapping[str, Mapping[str, Any]],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
    *,
    effect_bf_threshold: float = 3.0,
    no_effect_bf_threshold: float = 1 / 3,
    tau_near_zero_threshold: float = 0.1,
    monotone_prior_scale: float = math.sqrt(2) / 2,
    monotone_increment_samples: int = 512,
    monotone_prior_grid_points: int = 257,
    monotone_direction_probability_threshold: float = 0.95,
) -> List[Dict[str, Any]]:
    score_rows = behavior_score_rows(blind_reviews_by_id, matched_configurations_by_id, selected_hypothesis_ids)
    rows_by_hypothesis = _rows_by_hypothesis(score_rows)
    out = []
    for hypothesis_id in selected_hypothesis_ids:
        config_design = matched_configurations_by_id.get(hypothesis_id, {})
        hypothesis_rows = rows_by_hypothesis.get(hypothesis_id, [])
        analysis = _analyze_hypothesis_effect(
            hypothesis_rows,
            effect_bf_threshold=effect_bf_threshold,
            no_effect_bf_threshold=no_effect_bf_threshold,
            tau_near_zero_threshold=tau_near_zero_threshold,
            monotone_prior_scale=monotone_prior_scale,
            monotone_increment_samples=monotone_increment_samples,
            monotone_prior_grid_points=monotone_prior_grid_points,
            monotone_direction_probability_threshold=monotone_direction_probability_threshold,
        )
        out.append(
            {
                "axis_slug": hypothesis_id,
                "variable": config_design.get("variable"),
                "n": len(hypothesis_rows),
                **analysis,
            }
        )
    return out


def evidence_class_effect_rows(
    blind_reviews_by_id: Mapping[str, Mapping[str, Any]],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
    *,
    effect_bf_threshold: float = 3.0,
    no_effect_bf_threshold: float = 1 / 3,
    tau_near_zero_threshold: float = 0.1,
    monotone_prior_scale: float = math.sqrt(2) / 2,
    monotone_increment_samples: int = 512,
    monotone_prior_grid_points: int = 257,
    monotone_direction_probability_threshold: float = 0.95,
) -> List[Dict[str, Any]]:
    score_rows = behavior_evidence_class_score_rows(
        blind_reviews_by_id,
        matched_configurations_by_id,
        selected_hypothesis_ids,
    )
    rows_by_hypothesis_class: Dict[tuple[str, str], List[Mapping[str, Any]]] = defaultdict(list)
    for row in score_rows:
        rows_by_hypothesis_class[(str(row["axis_slug"]), str(row["evidence_class"]))].append(row)

    out = []
    for hypothesis_id in selected_hypothesis_ids:
        config_design = matched_configurations_by_id.get(hypothesis_id, {})
        evidence_classes = sorted(
            evidence_class
            for stored_hypothesis_id, evidence_class in rows_by_hypothesis_class
            if stored_hypothesis_id == hypothesis_id
        )
        for evidence_class in evidence_classes:
            rows = rows_by_hypothesis_class[(hypothesis_id, evidence_class)]
            analysis = _analyze_hypothesis_effect(
                rows,
                effect_bf_threshold=effect_bf_threshold,
                no_effect_bf_threshold=no_effect_bf_threshold,
                tau_near_zero_threshold=tau_near_zero_threshold,
                monotone_prior_scale=monotone_prior_scale,
                monotone_increment_samples=monotone_increment_samples,
                monotone_prior_grid_points=monotone_prior_grid_points,
                monotone_direction_probability_threshold=monotone_direction_probability_threshold,
            )
            out.append(
                {
                    "axis_slug": hypothesis_id,
                    "variable": config_design.get("variable"),
                    "outcome": evidence_class,
                    "n": len(rows),
                    **analysis,
                }
            )
    return out


def effect_analysis_rows(
    blind_reviews_by_id: Mapping[str, Mapping[str, Any]],
    matched_configurations_by_id: Mapping[str, Mapping[str, Any]],
    selected_hypothesis_ids: Sequence[str],
    *,
    effect_bf_threshold: float = 3.0,
    no_effect_bf_threshold: float = 1 / 3,
    tau_near_zero_threshold: float = 0.1,
    monotone_prior_scale: float = math.sqrt(2) / 2,
    monotone_increment_samples: int = 512,
    monotone_prior_grid_points: int = 257,
    monotone_direction_probability_threshold: float = 0.95,
) -> List[Dict[str, Any]]:
    aggregate_rows = hypothesis_effect_rows(
        blind_reviews_by_id,
        matched_configurations_by_id,
        selected_hypothesis_ids,
        effect_bf_threshold=effect_bf_threshold,
        no_effect_bf_threshold=no_effect_bf_threshold,
        tau_near_zero_threshold=tau_near_zero_threshold,
        monotone_prior_scale=monotone_prior_scale,
        monotone_increment_samples=monotone_increment_samples,
        monotone_prior_grid_points=monotone_prior_grid_points,
        monotone_direction_probability_threshold=monotone_direction_probability_threshold,
    )
    evidence_rows = evidence_class_effect_rows(
        blind_reviews_by_id,
        matched_configurations_by_id,
        selected_hypothesis_ids,
        effect_bf_threshold=effect_bf_threshold,
        no_effect_bf_threshold=no_effect_bf_threshold,
        tau_near_zero_threshold=tau_near_zero_threshold,
        monotone_prior_scale=monotone_prior_scale,
        monotone_increment_samples=monotone_increment_samples,
        monotone_prior_grid_points=monotone_prior_grid_points,
        monotone_direction_probability_threshold=monotone_direction_probability_threshold,
    )
    return [
        {
            **row,
            "outcome": "aggregate_mean",
        }
        for row in aggregate_rows
    ] + evidence_rows
