# ml/preprocess.py

import pandas as pd


def load_data(path):
    df = pd.read_csv(path)

    # Convert datetime
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # Drop invalid rows
    df = df.dropna(subset=["datetime"])

    # Sort by time
    df = df.sort_values("datetime").reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = load_data("../data/raw/synthetic_energy_data.csv")
    print("Data Loaded Successfully")
    print(df.head())