import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score
import joblib
import os
from data_preprocessing import load_and_preprocess

def train_models(data_path):
    # Load preprocessed data
    (X_train, X_test, 
     y_reg_train, y_reg_test, 
     y_clf_train, y_clf_test) = load_and_preprocess(data_path)
    
    print("\n" + "="*50)
    print("🎯 TRAINING REGRESSION MODEL")
    print("="*50)
    
    # Regression Model (Predict exact grade G3)
    regressor = RandomForestRegressor(
        n_estimators=100, 
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    regressor.fit(X_train, y_reg_train)
    
    # Quick validation
    y_reg_pred = regressor.predict(X_test)
    mae = mean_absolute_error(y_reg_test, y_reg_pred)
    r2 = r2_score(y_reg_test, y_reg_pred)
    
    print(f"✅ Random Forest Regressor trained!")
    print(f"   MAE: {mae:.2f} (avg error in grade points)")
    print(f"   R²:  {r2:.3f}")
    
    # Save model
    joblib.dump(regressor, 'models/grade_regressor.pkl')
    print(f"💾 Saved to models/grade_regressor.pkl")
    
    print("\n" + "="*50)
    print("🎯 TRAINING CLASSIFICATION MODEL")
    print("="*50)
    
    # Classification Model (Predict pass/fail)
    classifier = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    classifier.fit(X_train, y_clf_train)
    
    # Quick validation
    y_clf_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_clf_test, y_clf_pred)
    
    print(f"✅ Random Forest Classifier trained!")
    print(f"   Accuracy: {accuracy:.1%}")
    
    # Save model
    joblib.dump(classifier, 'models/pass_classifier.pkl')
    print(f"💾 Saved to models/pass_classifier.pkl")
    
    print("\n" + "="*50)
    print("✅ ALL MODELS TRAINED AND SAVED!")
    print("="*50)
    
    return X_test, y_reg_test, y_clf_test

if __name__ == "__main__":
    train_models('data/student-mat.csv')