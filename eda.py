import os

import numpy as np
import pandas as pd

# Name fragments that usually identify a binary target column
TARGET_KEYWORDS = [
    "label", "target", "class", "attack", "intrusion", "fraud", "churn",
    "outcome", "potab", "survived", "default",
]


def run_eda(filepath: str) -> dict:
    """
    Performs automatic Exploratory Data Analysis on a CSV dataset.
    Returns a structured summary dictionary for the AI report generator.
    """
    df = pd.read_csv(filepath)

    # Drop index columns saved by mistake (e.g. "Unnamed: 0")
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed:")]

    print(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")

    summary = {}

    # --- Basic Info ---
    summary["dataset_name"] = os.path.basename(filepath)
    summary["rows"] = df.shape[0]
    summary["columns"] = df.shape[1]
    summary["column_names"] = list(df.columns)

    # --- Data Types ---
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Everything that is not numeric, boolean or a date is treated as categorical.
    # This works with both the object dtype (pandas 2) and the str dtype (pandas 3).
    categorical_cols = df.select_dtypes(exclude=[np.number, "bool", "datetime"]).columns.tolist()
    summary["numeric_columns"] = numeric_cols
    summary["categorical_columns"] = categorical_cols

    # --- Missing Values ---
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_info = {col: f"{missing[col]} ({missing_pct[col]}%)" for col in df.columns if missing[col] > 0}
    summary["missing_values"] = missing_info if missing_info else "No missing values found"
    print(f"Missing values: {len(missing_info)} columns affected" if missing_info else "Missing values: none")

    # --- Duplicates ---
    duplicates = df.duplicated().sum()
    summary["duplicate_rows"] = int(duplicates)
    print(f"Duplicate rows: {duplicates}")

    # --- Numeric Stats ---
    if numeric_cols:
        stats = df[numeric_cols].describe().round(3)
        summary["numeric_stats"] = stats.to_dict()

        # Detect potential outliers using IQR
        outlier_info = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)).sum()
            if outliers > 0:
                outlier_info[col] = int(outliers)
        summary["outliers"] = outlier_info if outlier_info else "No significant outliers detected"

    # --- Categorical Stats ---
    if categorical_cols:
        cat_summary = {}
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            if value_counts.empty:
                continue
            cat_summary[col] = {
                "unique_values": int(df[col].nunique()),
                "top_value": str(value_counts.index[0]),
                "top_frequency": int(value_counts.iloc[0]),
                "top_5": value_counts.head(5).to_dict()
            }
        summary["categorical_stats"] = cat_summary

    # --- Correlation (numeric only) ---
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr().round(3)
        # Find high correlations (> 0.7, excluding self-correlation)
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                val = corr_matrix.iloc[i, j]
                if abs(val) > 0.7:
                    high_corr.append({
                        "col1": corr_matrix.columns[i],
                        "col2": corr_matrix.columns[j],
                        "correlation": round(float(val), 3)
                    })
        summary["high_correlations"] = high_corr if high_corr else "No strong correlations found (threshold > 0.7)"

    # --- Class balance (if binary/low cardinality target detected) ---
    for col in df.columns:
        is_target_name = any(keyword in col.lower() for keyword in TARGET_KEYWORDS)
        if df[col].nunique() == 2 and is_target_name:
            balance = df[col].value_counts(normalize=True).round(3).to_dict()
            summary["target_column"] = col
            summary["class_balance"] = balance
            print(f"Target column detected: '{col}' — Balance: {balance}")
            break

    print("EDA complete")
    return summary
