# ml/predict.py

import joblib
import os
import pandas as pd
import numpy as np

from ml.feature_engineering import create_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

TARIFF_RATE = 6  # ₹ per kWh


# -----------------------------
# Load Model
# -----------------------------
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("model.pkl not found inside ml folder.")
    return joblib.load(MODEL_PATH)


# -----------------------------
# Stable 24-Hour Forecast
# -----------------------------
def forecast_next_24_hours(df, model):

    working_df = create_features(df.copy())

    if working_df.empty:
        raise ValueError("Not enough historical data for future forecasting.")

    features = [
        "hour",
        "weekday",
        "month",
        "day_of_year",
        "lag_1",
        "lag_24",
        "rolling_mean_3",
        "rolling_mean_24",
    ]

    forecast_results = []

    for _ in range(24):

        last_row = working_df.iloc[-1]
        next_time = last_row["datetime"] + pd.Timedelta(hours=1)

        new_row = {
            "datetime": next_time,
            "hour": next_time.hour,
            "weekday": next_time.weekday(),
            "month": next_time.month,
            "day_of_year": next_time.dayofyear,
            "lag_1": last_row["energy_usage_kWh"],
            "lag_24": working_df.iloc[-24]["energy_usage_kWh"]
            if len(working_df) >= 24
            else last_row["energy_usage_kWh"],
            "rolling_mean_3": working_df["energy_usage_kWh"].tail(3).mean(),
            "rolling_mean_24": working_df["energy_usage_kWh"].tail(24).mean(),
        }

        X_future = pd.DataFrame([new_row])[features]

        prediction = model.predict(X_future)[0]

        new_row["energy_usage_kWh"] = prediction

        working_df = pd.concat(
            [working_df, pd.DataFrame([new_row])],
            ignore_index=True
        )

        forecast_results.append({
            "datetime": str(next_time),
            "predicted_energy_kWh": round(float(prediction), 2),
            "predicted_cost": round(float(prediction * TARIFF_RATE), 2)
        })

    return forecast_results


# -----------------------------
# Monthly Projection
# -----------------------------
def estimate_next_month_usage(processed_df):

    processed_df["date"] = processed_df["datetime"].dt.date

    daily_usage = processed_df.groupby("date")["energy_usage_kWh"].sum()

    last_7_days_avg = daily_usage.tail(7).mean()

    estimated_month_usage = last_7_days_avg * 30

    estimated_month_cost = estimated_month_usage * TARIFF_RATE

    return round(estimated_month_usage), round(estimated_month_cost)


# -----------------------------
# Main Prediction Function
# -----------------------------
def predict_from_dataframe(df):

    if df.empty:
        raise ValueError("Uploaded dataset is empty.")

    model = load_model()

    processed_df = create_features(df.copy())

    if processed_df.empty:
        raise ValueError(
            "Not enough historical data after feature engineering. "
            "Please upload minimum 48 continuous hourly records."
        )

    features = [
        "hour",
        "weekday",
        "month",
        "day_of_year",
        "lag_1",
        "lag_24",
        "rolling_mean_3",
        "rolling_mean_24",
    ]

    X = processed_df[features]

    predictions = model.predict(X)

    processed_df["predicted_energy_kWh"] = predictions

    processed_df["predicted_cost"] = (
        processed_df["predicted_energy_kWh"] * TARIFF_RATE
    )

    # Anomaly Detection
    processed_df["error"] = abs(
        processed_df["energy_usage_kWh"]
        - processed_df["predicted_energy_kWh"]
    )

    threshold = (
        processed_df["error"].mean()
        + 2 * processed_df["error"].std()
    )

    processed_df["anomaly"] = processed_df["error"] > threshold

    # 24 Hour Forecast
    future_forecast = forecast_next_24_hours(df, model)

    # Monthly Projection
    estimated_month_usage, estimated_month_cost = estimate_next_month_usage(
        processed_df
    )

    result = {
        "message": "Prediction completed successfully",
        "total_rows": int(len(processed_df)),
        "total_anomalies": int(processed_df["anomaly"].sum()),
        "estimated_total_cost": round(float(processed_df["predicted_cost"].sum())),
        "next_24_hours_forecast": future_forecast,
        "estimated_next_month_usage_kWh": estimated_month_usage,
        "estimated_next_month_cost": estimated_month_cost,
    }

    return result