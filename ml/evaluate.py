# ml/evaluate.py

import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ml.preprocess import load_data
from ml.feature_engineering import create_features


def evaluate_model():

    # Load data
    df = load_data("../data/raw/synthetic_energy_data.csv")
    df = create_features(df)

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

    X = df[features]
    y = df["energy_usage_kWh"]

    split = int(len(df) * 0.8)

    X_test = X[split:]
    y_test = y[split:]

    # Load model
    model = joblib.load("model.pkl")

    y_pred = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("MAE:", mae)
    print("RMSE:", rmse)
    print("R2:", r2)

    # Anomaly detection
    errors = abs(y_test.values - y_pred)
    threshold = errors.mean() + 2 * errors.std()

    anomalies = errors > threshold
    print("Total anomalies detected:", anomalies.sum())

    # Price prediction
    tariff_rate = 6
    predicted_cost = y_pred * tariff_rate

    print("Sample predicted cost:", predicted_cost[:5])


if __name__ == "__main__":
    evaluate_model()