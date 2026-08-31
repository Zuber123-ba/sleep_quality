# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import numpy as np

# 1️⃣ Load dataset
data_path = os.path.join("data", "raw", "sample_sleep_data.csv")
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Input CSV not found at {data_path}!")

df = pd.read_csv(data_path)
print("Columns in input dataset:", df.columns)

# 2️⃣ Target column
TARGET_COLUMN = "sleep_quality"
if TARGET_COLUMN not in df.columns:
    print(f"⚠️ Target column '{TARGET_COLUMN}' not found. Creating temporary target for testing...")
    df[TARGET_COLUMN] = np.random.randint(0, 2, size=len(df))

X = df.drop(TARGET_COLUMN, axis=1)
y = df[TARGET_COLUMN]

# 3️⃣ Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4️⃣ Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5️⃣ Save model
os.makedirs("models", exist_ok=True)
model_path = os.path.join("models", "sleep_model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Model trained and saved at {model_path}")
