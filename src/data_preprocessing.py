import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

def load_and_preprocess(filepath):
    print("📂 Loading dataset...")
    
    # Load data
    df = pd.read_csv(filepath, sep=';')
    print(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
    
    # Create binary target for classification (Pass if G3 >= 10)
    df['pass_fail'] = (df['G3'] >= 10).astype(int)
    print(f"📊 Pass rate: {df['pass_fail'].mean():.1%}")
    
    # Encode categorical variables
    categorical_cols = df.select_dtypes(include=['object']).columns
    label_encoders = {}
    
    print("🔤 Encoding categorical variables...")
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
        print(f"  - {col}: {len(le.classes_)} categories")
    
    # Features and targets
    X = df.drop(['G3', 'pass_fail'], axis=1)
    y_reg = df['G3']           # Regression target (final grade 0-20)
    y_clf = df['pass_fail']    # Classification target (0=Fail, 1=Pass)
    
    # Split data (80% train, 20% test)
    X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
        X, y_reg, y_clf, test_size=0.2, random_state=42, stratify=y_clf
    )
    
    print(f"\n📈 Training set: {len(X_train)} samples")
    print(f"📈 Test set: {len(X_test)} samples")
    
    # Scale features
    print("\n⚖️  Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save preprocessors
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(label_encoders, 'models/label_encoders.pkl')
    joblib.dump(list(X.columns), 'models/feature_names.pkl')
    
    print("✅ Preprocessing complete!")
    
    return (X_train_scaled, X_test_scaled, 
            y_reg_train, y_reg_test, 
            y_clf_train, y_clf_test)

if __name__ == "__main__":
    load_and_preprocess('data/student-mat.csv')