import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor


def prepare_monthly_data(df):
    data = df.copy()

    data["order_date"] = pd.to_datetime(
        data["order_date"]
    )

    monthly = (
        data.set_index("order_date")
        .resample("MS")["revenue"]
        .sum()
        .astype(float)
    )

    # Exclude an incomplete final calendar month.
    latest_date = data["order_date"].max()

    if latest_date.day < latest_date.days_in_month:
        monthly = monthly.iloc[:-1]

    return monthly


def make_features(series):
    frame = pd.DataFrame({"revenue": series})

    frame["lag_1"] = frame["revenue"].shift(1)
    frame["lag_2"] = frame["revenue"].shift(2)
    frame["lag_3"] = frame["revenue"].shift(3)

    frame["rolling_mean_3"] = (
        frame["revenue"]
        .shift(1)
        .rolling(3)
        .mean()
    )

    frame["month"] = frame.index.month
    frame["quarter"] = frame.index.quarter

    return frame.dropna()


FEATURES = [
    "lag_1",
    "lag_2",
    "lag_3",
    "rolling_mean_3",
    "month",
    "quarter"
]


def train_models(monthly):
    frame = make_features(monthly)

    if len(frame) < 8:
        raise ValueError(
            "At least 11 complete months are needed "
            "for model training and evaluation."
        )

    test_size = max(2, int(len(frame) * 0.2))

    train = frame.iloc[:-test_size]
    test = frame.iloc[-test_size:]

    models = {
        "Random Forest": RandomForestRegressor(
            n_estimators=150,
            max_depth=6,
            random_state=42
        ),
        "XGBoost": XGBRegressor(
            n_estimators=150,
            max_depth=3,
            learning_rate=0.05,
            objective="reg:squarederror",
            random_state=42
        )
    }

    scores = {
        "Naive Baseline": mean_absolute_error(
            test["revenue"],
            test["lag_1"]
        )
    }

    for name, model in models.items():
        model.fit(
            train[FEATURES],
            train["revenue"]
        )

        predictions = np.maximum(
            model.predict(test[FEATURES]),
            0
        )

        scores[name] = mean_absolute_error(
            test["revenue"],
            predictions
        )

    best_name = min(scores, key=scores.get)

    if best_name == "Naive Baseline":
        return None, best_name, scores

    best_model = models[best_name]

    best_model.fit(
        frame[FEATURES],
        frame["revenue"]
    )

    return best_model, best_name, scores


def forecast_revenue(monthly, model, months=3):
    history = monthly.astype(float).tolist()
    dates = []
    predictions = []

    for i in range(months):
        next_date = (
            monthly.index[-1]
            + pd.DateOffset(months=i + 1)
        )

        features = pd.DataFrame([{
            "lag_1": history[-1],
            "lag_2": history[-2],
            "lag_3": history[-3],
            "rolling_mean_3": np.mean(history[-3:]),
            "month": next_date.month,
            "quarter": next_date.quarter
        }])

        if model is None:
            prediction = history[-1]
        else:
            prediction = float(
                model.predict(features[FEATURES])[0]
            )

        prediction = max(0, prediction)

        history.append(prediction)
        dates.append(next_date)
        predictions.append(prediction)

    return pd.DataFrame({
        "month": dates,
        "predicted_revenue": predictions
    })
