"""Evaluate the trained model and produce metrics and plots."""
import joblib
import os
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import matplotlib.pyplot as plt
import numpy as np

MODEL = os.path.join(os.path.dirname(__file__), '..', 'models', 'sleep_model.pkl')
DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'test_sample.csv')
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'results')

def load():
    if not os.path.exists(MODEL):
        raise FileNotFoundError("Model not found. Run model_training first.")
    model = joblib.load(MODEL)
    if not os.path.exists(DATA):
        raise FileNotFoundError("test_sample.csv not found. Run model_training to generate it.")
    df = pd.read_csv(DATA)
    X = df.drop(columns=['label'])
    y = df['label']
    return model, X, y

if __name__ == '__main__':
    os.makedirs(OUT_DIR, exist_ok=True)
    model, X, y = load()
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:,1]

    print('Classification Report:')
    print(classification_report(y, y_pred))

    print('ROC AUC:', roc_auc_score(y, y_proba))

    # Confusion matrix
    cm = confusion_matrix(y, y_pred)
    fig, ax = plt.subplots()
    ax.matshow(cm, cmap='Blues')
    for (i, j), val in np.ndenumerate(cm):
        ax.text(j, i, str(val), ha='center', va='center')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.savefig(os.path.join(OUT_DIR, 'confusion_matrix.png'))
    print('Saved confusion matrix')

    # ROC curve
    fpr, tpr, _ = roc_curve(y, y_proba)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('ROC Curve')
    plt.savefig(os.path.join(OUT_DIR, 'roc_curve.png'))
    print('Saved ROC curve')
