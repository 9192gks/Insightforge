from pathlib import Path
import pandas as pd
import numpy as np

SUPPORTED = {".csv", ".xlsx", ".xls"}

def load_dataframe(path: str) -> pd.DataFrame:
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError("Unsupported file type. Use CSV or Excel.")

def profile(df):
    columns = []
    for c in df.columns:
        s = df[c]
        sample = []
        for x in s.dropna().head(5).tolist():
            if isinstance(x, (np.integer, np.floating)):
                sample.append(float(x))
            else:
                sample.append(str(x))
        columns.append({
            "name": str(c),
            "dtype": str(s.dtype),
            "missing": int(s.isna().sum()),
            "missing_pct": round(float(s.isna().mean() * 100), 2),
            "unique": int(s.nunique(dropna=True)),
            "sample": sample
        })
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_mb": round(float(df.memory_usage(deep=True).sum() / 1024**2), 3),
        "column_profiles": columns
    }

def numeric_correlations(df, threshold=-1):
    numeric = df.select_dtypes(include=np.number)
    if numeric.shape[1] < 2:
        return []
    corr = numeric.corr()
    result = []
    cols = list(corr.columns)
    for i, a in enumerate(cols):
        for b in cols[i+1:]:
            value = corr.loc[a, b]
            if pd.notna(value) and abs(value) >= threshold:
                result.append({
                    "column_a": str(a),
                    "column_b": str(b),
                    "correlation": round(float(value), 6)
                })
    return sorted(result, key=lambda x: abs(x["correlation"]), reverse=True)
