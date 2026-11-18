import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df, contamination=0.05):
    data = df.copy()

    features = [
        "quantity",
        "price_per_unit",
        "cost_per_unit",
        "revenue",
        "profit"
    ]

    if len(data) < 20:
        raise ValueError(
            "At least 20 transactions are required."
        )

    X = data[features].replace(
        [np.inf, -np.inf], np.nan
    )

    valid = X.notna().all(axis=1)

    data["anomaly"] = False
    data["anomaly_score"] = np.nan

    if valid.sum() < 20:
        raise ValueError(
            "At least 20 valid transactions are required."
        )

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42
    )

    predictions = model.fit_predict(X.loc[valid])
    scores = model.decision_function(X.loc[valid])

    data.loc[valid, "anomaly"] = predictions == -1
    data.loc[valid, "anomaly_score"] = scores

    return data.sort_values(
        "anomaly_score",
        ascending=True,
        na_position="last"
    )
