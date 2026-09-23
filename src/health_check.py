"""
Dataset health checks for MLPilot.
"""

import pandas as pd


def health_check(df):
    """
    Analyze a dataset and return health summary, warnings, and status.
    """
    
    missing_percent = (df.isnull().sum() / len(df)) * 100
    duplicate_rows = df.duplicated().sum()

    unique_counts = df.nunique()
    constant_cols = unique_counts[unique_counts == 1]

    unique_percent = (unique_counts / len(df)) * 100
    id_like_cols = unique_percent[unique_percent > 90]

    empty_cols = df.columns[df.isnull().all()]

    missing_cols = df.columns[df.isnull().any()]

    rows = len(df)
    columns = len(df.columns)

    health_summary = {
    "rows": rows,
    "columns": columns,
    "duplicate_rows": duplicate_rows,
    "missing_columns": len(missing_cols),
    "constant_columns": len(constant_cols),
    "id_like_columns": len(id_like_cols),
    "id_like_column_names": list(id_like_cols.index),
    "empty_columns": len(empty_cols),
    "missing_column_names": list(missing_cols),
    "constant_column_names": list(constant_cols.index),
    "empty_column_names": list(empty_cols)
    }

    warnings = []
    serious_issues = 0
    if duplicate_rows > 0:
        warnings.append(
        f"{duplicate_rows} duplicate rows found."
            )

    if len(missing_cols) > 0:
        
        warnings.append(
        f"{len(missing_cols)} columns contain missing values."
            )

    if len(constant_cols) > 0:
        warnings.append(
        f"{len(constant_cols)} constant columns found."
            )
    if len(id_like_cols) > 0:
        warnings.append(
        f"{len(id_like_cols)} possible ID-like columns found."
            )

    if len(empty_cols) > 0:
        warnings.append(
        f"{len(empty_cols)} completely empty columns found."
            )

    for col in df.columns:
        pct = missing_percent[col]

        if pct >= 50:
            serious_issues += 1
            
            warnings.append(
            f"🔴 {col} has {pct:.1f}% missing values."
        )
        elif pct > 0:
            warnings.append(
            f"🟡 {col} has {pct:.1f}% missing values."
        )
    if serious_issues > 0:
        health_status = "Poor"
    elif len(warnings) > 0:
        health_status = "Needs Attention"
    else:
        health_status = "Healthy"

    return {
    "summary": health_summary,
    "warnings": warnings,
    "status": health_status
    }
    