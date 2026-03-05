# ml/feature_engineering.py

import pandas as pd


def create_features(df):

    # Time features
    df["hour"] = df["datetime"].dt.hour
    df["weekday"] = df["datetime"].dt.weekday
    df["month"] = df["datetime"].dt.month
    df["day_of_year"] = df["datetime"].dt.dayofyear

    # Lag features
    df["lag_1"] = df["energy_usage_kWh"].shift(1)
    df["lag_24"] = df["energy_usage_kWh"].shift(24)

    # Rolling features
    df["rolling_mean_3"] = df["energy_usage_kWh"].rolling(3).mean()
    df["rolling_mean_24"] = df["energy_usage_kWh"].rolling(24).mean()

    # Drop NaN rows
    df = df.dropna().reset_index(drop=True)

    return df


if __name__ == "__main__":
    from preprocess import load_data

    df = load_data("../data/raw/synthetic_energy_data.csv")
    df = create_features(df)

    print("Features Created Successfully")
    print(df.head())