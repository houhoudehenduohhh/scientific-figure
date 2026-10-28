#!/usr/bin/env python3
"""Statistical assumption audit and test recommender for Nature-grade figures.

Performs:
1. Normality checks (Shapiro-Wilk for N <= 5000, D'Agostino-Pearson for N > 5000).
2. Homoscedasticity check (Levene's test with median centering).
3. Recommendation of parametric vs non-parametric hypothesis tests.
4. Calculation of descriptive statistics (N, Mean, SD, Median, IQR) and effect sizes.

Outputs machine-readable JSON or tabular summary for data contract integration.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from scipy import stats


def check_normality(data: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
    """Test normality of a 1D numerical array."""
    clean = data[~np.isnan(data)]
    n = len(clean)
    if n < 3:
        return {"test": "none", "stat": None, "p_val": None, "normal": False, "reason": "n < 3"}
    
    if n <= 5000:
        stat, p = stats.shapiro(clean)
        test_name = "Shapiro-Wilk"
    else:
        stat, p = stats.normaltest(clean)
        test_name = "D'Agostino-Pearson"
        
    return {
        "test": test_name,
        "stat": float(stat),
        "p_val": float(p),
        "normal": bool(p > alpha),
        "n": int(n)
    }


def check_homoscedasticity(*groups: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
    """Test homogeneity of variance across multiple groups using Levene's test."""
    clean_groups = [g[~np.isnan(g)] for g in groups if len(g[~np.isnan(g)]) >= 2]
    if len(clean_groups) < 2:
        return {"test": "Levene", "stat": None, "p_val": None, "equal_var": False, "reason": "insufficient groups"}
    
    stat, p = stats.levene(*clean_groups, center="median")
    return {
        "test": "Levene (median)",
        "stat": float(stat),
        "p_val": float(p),
        "equal_var": bool(p > alpha)
    }


def audit_groups(
    df: pd.DataFrame,
    value_col: str,
    group_col: str,
    alpha: float = 0.05
) -> Dict[str, Any]:
    """Audit assumptions across categorical groups in a DataFrame."""
    groups = df[group_col].dropna().unique()
    group_data: Dict[str, np.ndarray] = {}
    normality_results: Dict[str, Any] = {}
    summary_stats: Dict[str, Any] = {}
    
    all_normal = True
    for grp in groups:
        vals = df.loc[df[group_col] == grp, value_col].dropna().to_numpy(dtype=float)
        group_data[str(grp)] = vals
        norm_res = check_normality(vals, alpha=alpha)
        normality_results[str(grp)] = norm_res
        if not norm_res["normal"]:
            all_normal = False
            
        summary_stats[str(grp)] = {
            "n": int(len(vals)),
            "mean": float(np.mean(vals)) if len(vals) > 0 else None,
            "std": float(np.std(vals, ddof=1)) if len(vals) > 1 else None,
            "median": float(np.median(vals)) if len(vals) > 0 else None,
            "q25": float(np.percentile(vals, 25)) if len(vals) > 0 else None,
            "q75": float(np.percentile(vals, 75)) if len(vals) > 0 else None,
            "iqr": float(np.percentile(vals, 75) - np.percentile(vals, 25)) if len(vals) > 0 else None
        }
        
    homo_res = check_homoscedasticity(*group_data.values(), alpha=alpha)
    equal_var = homo_res["equal_var"]
    
    num_groups = len(groups)
    if num_groups == 2:
        if all_normal and equal_var:
            recommended_test = "Student's two-sample t-test"
            error_bar_rec = "Mean +/- SEM or Mean +/- 95% CI"
        elif all_normal and not equal_var:
            recommended_test = "Welch's t-test (unequal variances)"
            error_bar_rec = "Mean +/- SEM or Mean +/- 95% CI"
        else:
            recommended_test = "Mann-Whitney U test (non-parametric)"
            error_bar_rec = "Median with IQR (box plot or violin with quartiles)"
    elif num_groups > 2:
        if all_normal and equal_var:
            recommended_test = "One-way ANOVA with Tukey HSD post-hoc"
            error_bar_rec = "Mean +/- SEM"
        elif all_normal and not equal_var:
            recommended_test = "Welch's ANOVA with Games-Howell post-hoc"
            error_bar_rec = "Mean +/- SEM"
        else:
            recommended_test = "Kruskal-Wallis H test with Dunn's post-hoc"
            error_bar_rec = "Median with IQR"
    else:
        recommended_test = "Single group description / One-sample test"
        error_bar_rec = "Mean +/- SD"
        
    return {
        "value_column": value_col,
        "group_column": group_col,
        "num_groups": int(num_groups),
        "normality": normality_results,
        "all_groups_normal": bool(all_normal),
        "homoscedasticity": homo_res,
        "summary_statistics": summary_stats,
        "recommended_hypothesis_test": recommended_test,
        "recommended_visual_error_metric": error_bar_rec
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit statistical assumptions and recommend tests.")
    parser.add_argument("--data", required=True, type=Path, help="Path to input CSV or Parquet file.")
    parser.add_argument("--value", required=True, type=str, help="Name of the continuous value column.")
    parser.add_argument("--group", required=True, type=str, help="Name of the categorical grouping column.")
    parser.add_argument("--alpha", default=0.05, type=float, help="Significance threshold (default: 0.05).")
    parser.add_argument("--out", type=Path, default=None, help="Optional output JSON path.")
    
    args = parser.parse_args()
    
    if not args.data.exists():
        sys.stderr.write(f"Error: file not found: {args.data}\n")
        return 1
        
    if args.data.suffix.lower() == ".parquet":
        df = pd.read_parquet(args.data)
    else:
        df = pd.read_csv(args.data)
        
    if args.value not in df.columns:
        sys.stderr.write(f"Error: value column '{args.value}' not in columns {list(df.columns)}\n")
        return 1
    if args.group not in df.columns:
        sys.stderr.write(f"Error: group column '{args.group}' not in columns {list(df.columns)}\n")
        return 1
        
    report = audit_groups(df, args.value, args.group, alpha=args.alpha)
    formatted_json = json.dumps(report, indent=2)
    
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(formatted_json, encoding="utf-8")
        print(f"Audit report saved to: {args.out}")
    else:
        print(formatted_json)
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
