"""Load model and provide helper to predict on input dataframes."""

import joblib
import os
import pandas as pd

# ------------------------------
# 1️⃣ Set model path relative to this file
# ------------------------------

# Get the directory of this file and construct the model path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = os.path.join(BASE_DIR, "models", "sleep_model.pkl")

_model = None

# ------------------------------
# 2️⃣ Load model function
# ------------------------------
def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL):
            raise FileNotFoundError(f"Model not found at {MODEL}. Run train_model.py first.")
        _model = joblib.load(MODEL)
    return _model
def sleep_need_from_face(fatigue_score, age):
    if age <= 25:
        base_sleep = 8
    elif age <= 40:
        base_sleep = 7.5
    else:
        base_sleep = 7

    if fatigue_score > 20:
        base_sleep += 1

    return base_sleep

# ------------------------------
# 3️⃣ Predict helper
# ------------------------------
def predict_df(df: pd.DataFrame):
    """
    Returns predictions and probabilities as a DataFrame with columns:
    'prediction', 'probability'
    """
    model = load_model()
    X = df.copy()

    # Drop target if exists
    TARGET_COLUMN = "sleep_quality"
    if TARGET_COLUMN in X.columns:
        X = X.drop(columns=[TARGET_COLUMN])

    # Make predictions
    preds = model.predict(X)

    # If model supports predict_proba
    try:
        probs = model.predict_proba(X)[:, 1]
    except AttributeError:
        probs = [None]*len(preds)  # If model doesn't support probability

    # Return dataframe
    out = pd.DataFrame({
        'prediction': preds,
        'probability': probs
    })
    return out
