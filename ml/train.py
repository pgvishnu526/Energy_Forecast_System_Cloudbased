# ml/train.py

import joblib
from sklearn.ensemble import RandomForestRegressor

from ml.preprocess import load_data
from ml.feature_engineering import create_features


def train_model():

    # Load and process data
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

    # Time-based split
    split = int(len(df) * 0.8)

    X_train = X[:split]
    y_train = y[:split]

    X_test = X[split:]
    y_test = y[split:]

    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, "model.pkl")

    print("Model trained and saved successfully!")

    return X_test, y_test, model


if __name__ == "__main__":
    train_model()