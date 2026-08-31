"""Cleans raw CSV and outputs processed CSV."""
import pandas as pd
import numpy as np
import os

RAW = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'sleep_raw.csv')
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
OUT = os.path.join(OUT_DIR, 'sleep_clean.csv')

def load_data(path=RAW):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw CSV not found at {path}")
    df = pd.read_csv(path)
    return df

def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    # Strip column names
    df.columns = [c.strip() for c in df.columns]

    # Convert rating -> label if rating column exists (>=4 -> good=1)
    if 'rating' in df.columns and 'label' not in df.columns:
        df['label'] = df['rating'].apply(lambda x: 1 if x >= 4 else 0)

    # Drop rows without label
    if 'label' in df.columns:
        df = df.dropna(subset=['label'])

    # Fill numeric NaNs with median
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for c in num_cols:
        df[c] = df[c].fillna(df[c].median())

    # Fill categorical missing with mode or empty string
    cat_cols = df.select_dtypes(include=['object','category','bool']).columns.tolist()
    for c in cat_cols:
        df[c] = df[c].fillna(df[c].mode().iloc[0] if not df[c].mode().empty else '')

    # Keep essential columns only (optional)
    return df

def save(df: pd.DataFrame, path=OUT):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved processed data to {path}")

if __name__ == '__main__':
    print('Loading raw data...')
    df = load_data()
    print('Running basic clean...')
    df = basic_clean(df)
    save(df)
