import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

def detect(df, limit=100):
    numeric = df.select_dtypes(include=np.number)
    if numeric.shape[1] == 0 or len(df) < 20:
        return []

    clean = numeric.replace([np.inf, -np.inf], np.nan)
    clean = clean.fillna(clean.median()).fillna(0)

    contamination = min(max(5 / len(df), 0.005), 0.08)
    model = IsolationForest(
        n_estimators=150,
        contamination=contamination,
        random_state=42,
        n_jobs=-1
    )
    labels = model.fit_predict(clean)
    scores = model.decision_function(clean)

    positions = np.where(labels == -1)[0]
    positions = sorted(positions, key=lambda i: scores[i])

    result = []
    for i in positions[:limit]:
        row = {}
        for c, v in df.iloc[i].items():
            if pd.isna(v):
                row[c] = None
            elif isinstance(v, np.generic):
                row[c] = v.item()
            else:
                row[c] = v
        result.append({
            "row_index": int(i),
            "anomaly_score": round(float(scores[i]), 6),
            "data": row
        })
    return result
