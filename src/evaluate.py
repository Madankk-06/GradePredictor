import joblib
import json
import os
import numpy as np
from sklearn.metrics import (mean_absolute_error, mean_squared_error, r2_score,
                            accuracy_score, classification_report, confusion_matrix)
from train_model import train_models

def evaluate_models():
    print("="*60)
    print("📊 MODEL EVALUATION")
    print("="*60)
    
    # Train and get test data
    X_test, y_reg_test, y_clf_test = train_models('data/student-mat.csv')
    
    # Load models
    regressor = joblib.load('models/grade_regressor.pkl')
    classifier = joblib.load('models/pass_classifier.pkl')
    
    # ==================== REGRESSION EVALUATION ====================
    print("\n" + "="*60)
    print("📈 REGRESSION RESULTS (Final Grade G3 Prediction)")
    print("="*60)
    
    y_reg_pred = regressor.predict(X_test)
    
    reg_metrics = {
        'MAE': round(mean_absolute_error(y_reg_test, y_reg_pred), 2),
        'RMSE': round(np.sqrt(mean_squared_error(y_reg_test, y_reg_pred)), 2),
        'R2_Score': round(r2_score(y_reg_test, y_reg_pred), 3)
    }
    
    print(f"Mean Absolute Error (MAE):        {reg_metrics['MAE']:.2f} points")
    print(f"Root Mean Squared Error (RMSE):   {reg_metrics['RMSE']:.2f} points")
    print(f"R² Score:                         {reg_metrics['R2_Score']:.3f}")
    print(f"\nInterpretation:")
    print(f"  • Predictions are off by ~{reg_metrics['MAE']:.1f} grade points on average")
    print(f"  • Model explains {reg_metrics['R2_Score']*100:.1f}% of grade variance")
    
    # ==================== CLASSIFICATION EVALUATION ====================
    print("\n" + "="*60)
    print("📊 CLASSIFICATION RESULTS (Pass/Fail Prediction)")
    print("="*60)
    
    y_clf_pred = classifier.predict(X_test)
    y_clf_proba = classifier.predict_proba(X_test)[:, 1]
    
    accuracy = accuracy_score(y_clf_test, y_clf_pred)
    cm = confusion_matrix(y_clf_test, y_clf_pred)
    
    print(f"Accuracy:  {accuracy:.1%}")
    print(f"\nConfusion Matrix:")
    print(f"                 Predicted")
    print(f"                 Fail   Pass")
    print(f"Actual Fail      {cm[0,0]:3d}    {cm[0,1]:3d}")
    print(f"       Pass      {cm[1,0]:3d}    {cm[1,1]:3d}")
    
    print(f"\nClassification Report:")
    print(classification_report(y_clf_test, y_clf_pred, 
                               target_names=['Fail (0-9)', 'Pass (10-20)']))
    
    # ==================== SAVE RESULTS ====================
    print("\n" + "="*60)
    print("💾 SAVING RESULTS")
    print("="*60)
    
    # Save regression metrics
    with open('results/regression_metrics.txt', 'w') as f:
        json.dump(reg_metrics, f, indent=2)
    print("✅ Saved: results/regression_metrics.txt")
    
    # Save classification report
    clf_report = classification_report(y_clf_test, y_clf_pred, 
                                      target_names=['Fail', 'Pass'])
    with open('results/classification_report.txt', 'w') as f:
        f.write(f"Accuracy: {accuracy:.3f}\n\n")
        f.write("Confusion Matrix:\n")
        f.write(f"TN={cm[0,0]}, FP={cm[0,1]}\n")
        f.write(f"FN={cm[1,0]}, TP={cm[1,1]}\n\n")
        f.write(clf_report)
    print("✅ Saved: results/classification_report.txt")
    
    print("\n" + "="*60)
    print("✅ EVALUATION COMPLETE!")
    print("="*60)
    
    return reg_metrics, accuracy

if __name__ == "__main__":
    evaluate_models()