"""Feature engineering for sleep dataset."""
import pandas as pd
import numpy as np
import os

IN = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'sleep_clean.csv')
OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'sleep_features.csv')

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Sleep efficiency
    if 'total_sleep_minutes' in df.columns and 'wake_after_sleep_minutes' in df.columns:
        df['sleep_efficiency'] = (df['total_sleep_minutes'] - df['wake_after_sleep_minutes']) / (df['total_sleep_minutes'] + 1e-6)
    else:
        df['sleep_efficiency'] = df.get('sleep_efficiency', 0.8)

    # Latency ratio
    if 'sleep_latency' in df.columns and 'total_sleep_minutes' in df.columns:
        df['latency_ratio'] = df['sleep_latency'] / (df['total_sleep_minutes'] + 1e-6)
    else:
        df['latency_ratio'] = 0.01

    # Bedtime difference to median (if bedtime_minutes exists)
    if 'bedtime_minutes' in df.columns:
        median_bed = df['bedtime_minutes'].median()
        df['bedtime_diff'] = (df['bedtime_minutes'] - median_bed).abs()
    else:
        df['bedtime_diff'] = 0

    # Simple categorical encoding placeholders (not applied here)
    # Fill NaNs
    df = df.fillna(0)
    return df

if __name__ == '__main__':
    if not os.path.exists(IN):
        raise FileNotFoundError(f"Processed file not found at {IN}. Run data_preprocessing first or place sleep_clean.csv there.")
    df = pd.read_csv(IN)
    df2 = add_features(df)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    df2.to_csv(OUT, index=False)
    print(f"Saved feature-engineered data to {OUT}")
