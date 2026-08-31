# test_predict.py
import pandas as pd
import os
import pickle

# ------------------------------
# 1️⃣ Load input CSV
# ------------------------------
data_path = os.path.join("data", "raw", "sample_sleep_data.csv")
df = pd.read_csv(data_path)
print("Columns in input dataset:", df.columns)

# ------------------------------
# 2️⃣ Load trained model
# ------------------------------
model_path = os.path.join("models", "sleep_model.pkl")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at {model_path}. Please run train_model.py first!")

with open(model_path, "rb") as f:
    model = pickle.load(f)

# ------------------------------
# 3️⃣ Prepare features
# ------------------------------
TARGET_COLUMN = "sleep_quality"
if TARGET_COLUMN in df.columns:
    X = df.drop(TARGET_COLUMN, axis=1)
else:
    X = df.copy()

# ------------------------------
# 4️⃣ Predict
# ------------------------------
preds = model.predict(X)

# Check if model supports probabilities
try:
    probs = model.predict_proba(X)[:, 1]
except AttributeError:
    probs = [None] * len(preds)

df["predicted_sleep_quality"] = preds
df["probability"] = probs

# ------------------------------
# 5️⃣ Map predictions to labels
# ------------------------------
def label_sleep_quality(row):
    if row['predicted_sleep_quality'] == 0:
        return "Bad"
    else:
        if row['probability'] is not None and row['probability'] >= 0.8:
            return "Best"
        else:
            return "Good"

df["predicted_sleep_quality_label"] = df.apply(label_sleep_quality, axis=1)

# ------------------------------
# 6️⃣ Save predictions
# ------------------------------
output_path = os.path.join("data", "raw", "predictions.csv")
df.to_csv(output_path, index=False)
print(f"✅ Predictions with labels saved to {output_path}")
print(df.head())
