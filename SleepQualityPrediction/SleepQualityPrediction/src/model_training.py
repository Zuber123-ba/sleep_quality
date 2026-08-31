"""Train an XGBoost classifier on processed data and save model + artifacts."""
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from xgboost import XGBClassifier
import joblib
import warnings
warnings.filterwarnings("ignore")

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'sleep_features.csv')
# fallback to sleep_clean if features not generated
if not os.path.exists(DATA):
    DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'sleep_clean.csv')

MODEL_OUT = os.path.join(os.path.dirname(__file__), '..', 'models', 'sleep_model.pkl')

def load_data(path=DATA):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Processed CSV not found at {path}")
    df = pd.read_csv(path)
    return df

def prepare_X_y(df: pd.DataFrame):
    df = df.copy()
    if 'label' not in df.columns:
        raise ValueError('Data must contain `label` column with 0/1 values')
    y = df['label']
    X = df.drop(columns=['label'])
    # Drop identifiers if present
    if 'user_id' in X.columns:
        X = X.drop(columns=['user_id'])
    if 'date' in X.columns:
        X = X.drop(columns=['date'])
    return X, y

def build_pipeline(X: pd.DataFrame):
    num_cols = X.select_dtypes(include=['int64','float64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object','category','bool']).columns.tolist()

    num_pipe = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
    cat_pipe = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('ohe', OneHotEncoder(handle_unknown='ignore'))])

    preproc = ColumnTransformer([('num', num_pipe, num_cols), ('cat', cat_pipe, cat_cols)])

    clf = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42, n_estimators=50)

    model = Pipeline([('preproc', preproc), ('clf', clf)])
    return model

if __name__ == '__main__':
    print('Loading processed data...')
    df = load_data()
    print('Preparing X and y...')
    X, y = prepare_X_y(df)
    print('Building pipeline...')
    model = build_pipeline(X)
    print('Splitting train/test...')
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
    print('Training model...')
    model.fit(X_train, y_train)
    os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)
    joblib.dump(model, MODEL_OUT)
    print(f'Model saved to {MODEL_OUT}')

    # Save a small test CSV for API quick test
    test_sample = X_test.copy()
    test_sample['label'] = y_test
    test_sample_path = os.path.join(os.path.dirname(__file__),'..','data','processed','test_sample.csv')
    test_sample.to_csv(test_sample_path, index=False)
    print(f'Saved test_sample to {test_sample_path}')
