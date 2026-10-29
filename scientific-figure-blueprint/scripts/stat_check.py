#!/usr/bin/env python3
"""Statistical assumption audit, data structure quality diagnostic, and test recommender.

Performs:
1. Data Structure Diagnostic: row/column count, memory footprint, data types, near-zero variance.
2. Missing Value Audit: missing counts/rates, complete-case retention, severity grading & strategy.
3. Outlier Inspection: percentiles (P1-P99.5), IQR Tukey bounds, skewness, truncation recommendations.
4. Statistical Assumption Checks: normality (Shapiro-Wilk / D'Agostino-Pearson) & homoscedasticity (Levene).
5. Hypothesis Test & Error Metric Recommendation.

Outputs machine-readable JSON or tabular summary for blueprint and data contract integration.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from scipy import stats


def audit_dataframe_quality(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    id_cols: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Audit dataset structure, missingness, and outliers for blueprint generation."""
    target_cols = columns if columns else list(df.columns)
    valid_cols = [c for c in target_cols if c in df.columns]
    
    total_rows = len(df)
    total_cols = len(df.columns)
    mem_mb = round(float(df.memory_usage(deep=True).sum()) / (1024 * 1024), 2)
    duplicate_rows = int(df.duplicated().sum())
    
    # 1. Structure overview
    cols_overview: Dict[str, Any] = {}
    for col in valid_cols:
        s = df[col]
        n_unique = int(s.nunique(dropna=True))
        is_const = bool(n_unique <= 1)
        
        # Near-zero variance check
        is_nzv = False
        if total_rows > 0 and n_unique > 1:
            val_counts = s.value_counts(dropna=True, ascending=False)
            if len(val_counts) >= 2:
                freq_ratio = float(val_counts.iloc[0] / max(1, val_counts.iloc[1]))
                percent_unique = float(n_unique / total_rows * 100)
                if freq_ratio > 19.0 and percent_unique < 10.0:
                    is_nzv = True
                    
        cols_overview[col] = {
            "dtype": str(s.dtype),
            "non_null_count": int(s.notna().sum()),
            "unique_count": n_unique,
            "is_constant": is_const,
            "is_near_zero_variance": is_nzv
        }

    # 2. Missing value audit
    missing_audit: Dict[str, Any] = {}
    actions: List[str] = []
    
    for col in valid_cols:
        miss_cnt = int(df[col].isna().sum())
        miss_pct = round(float(miss_cnt / total_rows * 100), 3) if total_rows > 0 else 0.0
        
        if miss_pct == 0.0:
            severity = "Zero (0%)"
            rec = "No action needed (100% complete)."
        elif miss_pct < 1.0:
            severity = "Low (<1%)"
            rec = "Safe for complete-case filtering. Ensure logging dropped row counts."
            actions.append(f"Column '{col}' has low missingness ({miss_pct}%); filter complete cases with logged count.")
        elif miss_pct <= 5.0:
            severity = "Moderate (1-5%)"
            rec = "Complete-case filtering acceptable if MCAR; consider median/mode imputation if sample size is limited."
            actions.append(f"Column '{col}' has moderate missingness ({miss_pct}%); confirm MCAR assumption before dropping.")
        elif miss_pct <= 20.0:
            severity = "High (5-20%)"
            rec = "High missingness: Multiple Imputation (MICE) or Missing Indicator method recommended to avoid bias."
            actions.append(f"Column '{col}' has high missingness ({miss_pct}%); use Multiple Imputation or Missing Indicator.")
        else:
            severity = "Severe (>20%)"
            rec = "Severe missingness: evaluate covariate necessity; consider excluding or conducting sensitivity analysis."
            actions.append(f"Column '{col}' has severe missingness ({miss_pct}%); evaluate excluding from primary model.")
            
        missing_audit[col] = {
            "missing_count": miss_cnt,
            "missing_pct": miss_pct,
            "severity": severity,
            "recommendation": rec
        }
        
    complete_case_n = int(df[valid_cols].dropna().shape[0]) if valid_cols else total_rows
    complete_case_pct = round(float(complete_case_n / total_rows * 100), 2) if total_rows > 0 else 100.0

    # 3. Outlier and distribution audit for numeric columns
    outlier_audit: Dict[str, Any] = {}
    for col in valid_cols:
        s = df[col].dropna()
        if not pd.api.types.is_numeric_dtype(df[col]) or len(s) < 3:
            continue
            
        vals = s.to_numpy(dtype=float)
        q25 = float(np.percentile(vals, 25))
        q75 = float(np.percentile(vals, 75))
        iqr = float(q75 - q25)
        p1 = float(np.percentile(vals, 1))
        p5 = float(np.percentile(vals, 5))
        p95 = float(np.percentile(vals, 95))
        p99 = float(np.percentile(vals, 99))
        p99_5 = float(np.percentile(vals, 99.5))
        val_min = float(np.min(vals))
        val_max = float(np.max(vals))
        val_mean = float(np.mean(vals))
        val_std = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
        val_median = float(np.median(vals))
        
        skew_raw = stats.skew(vals)
        skew = 0.0 if np.isnan(skew_raw) else float(skew_raw)
        if skew > 1.5:
            skew_desc = "Heavy right skew"
        elif skew < -1.5:
            skew_desc = "Heavy left skew"
        elif abs(skew) <= 0.5:
            skew_desc = "Approximately symmetric"
        else:
            skew_desc = "Moderate skew"
            
        tukey_lower = q25 - 1.5 * iqr
        tukey_upper = q75 + 1.5 * iqr
        tukey_outliers = int(np.sum((vals < tukey_lower) | (vals > tukey_upper)))
        p99_exceed = int(np.sum(vals > p99))
        
        # Recommendations
        if skew > 1.5 and val_max > p99 * 1.5:
            rec_trunc = "Enforce P99 / P99.5 upper Winsorization (capping) and consider log transformation ln(x+1)."
            actions.append(f"Column '{col}' is heavily right-skewed (skew={skew:.2f}, max={val_max:.2f} vs P99={p99:.2f}); enforce P99 Winsorization.")
        elif tukey_outliers > 0 and (val_min < 0 and "pct" in col.lower()):
            rec_trunc = "Negative values detected in percentage/ratio column; clean physical invalid values."
            actions.append(f"Column '{col}' has invalid negative values; clean before analysis.")
        elif p99_exceed > 0 and val_max > p99 * 1.2:
            rec_trunc = "Upper extreme tail detected; recommend P99 truncation to stabilize regression and visualization."
            actions.append(f"Column '{col}' has extreme upper tail (max={val_max:.2f} vs P99={p99:.2f}); recommend P99 truncation.")
        else:
            rec_trunc = "Distribution well-bounded; no truncation required."
            
        outlier_audit[col] = {
            "n": int(len(vals)),
            "mean": round(val_mean, 4),
            "std": round(val_std, 4),
            "min": round(val_min, 4),
            "p1": round(p1, 4),
            "p5": round(p5, 4),
            "q25": round(q25, 4),
            "median": round(val_median, 4),
            "q75": round(q75, 4),
            "p95": round(p95, 4),
            "p99": round(p99, 4),
            "p99_5": round(p99_5, 4),
            "max": round(val_max, 4),
            "iqr": round(iqr, 4),
            "skewness": round(skew, 3),
            "skewness_assessment": skew_desc,
            "tukey_bounds": [round(tukey_lower, 4), round(tukey_upper, 4)],
            "tukey_outliers_count": tukey_outliers,
            "p99_exceed_count": p99_exceed,
            "recommendation": rec_trunc
        }

    return {
        "dimensions": {
            "total_rows": total_rows,
            "total_columns": total_cols,
            "memory_usage_mb": mem_mb,
            "duplicate_rows": duplicate_rows
        },
        "complete_case_analysis": {
            "audited_columns_count": len(valid_cols),
            "complete_case_rows": complete_case_n,
            "complete_case_retention_pct": complete_case_pct,
            "rows_with_missingness": total_rows - complete_case_n
        },
        "columns_overview": cols_overview,
        "missing_audit": missing_audit,
        "outlier_audit": outlier_audit,
        "actionable_recommendations": actions
    }


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
    parser = argparse.ArgumentParser(description="Audit data quality, missingness, outliers, and statistical assumptions.")
    parser.add_argument("--data", required=True, type=Path, help="Path to input CSV or Parquet file.")
    parser.add_argument("--audit-data", action="store_true", help="Perform comprehensive data structure, missing, and outlier audit.")
    parser.add_argument("--cols", nargs="*", default=None, help="Specific columns to audit (default: all).")
    parser.add_argument("--value", type=str, default=None, help="Continuous value column for hypothesis testing audit.")
    parser.add_argument("--group", type=str, default=None, help="Grouping column for hypothesis testing audit.")
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

    report: Dict[str, Any] = {}

    # Comprehensive data structure audit
    if args.audit_data or (args.value is None and args.group is None):
        report["data_quality"] = audit_dataframe_quality(df, columns=args.cols)
        
    # Hypothesis testing audit if value & group are specified
    if args.value and args.group:
        if args.value not in df.columns:
            sys.stderr.write(f"Error: value column '{args.value}' not in columns {list(df.columns)}\n")
            return 1
        if args.group not in df.columns:
            sys.stderr.write(f"Error: group column '{args.group}' not in columns {list(df.columns)}\n")
            return 1
        report["hypothesis_testing_audit"] = audit_groups(df, args.value, args.group, alpha=args.alpha)
        
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
