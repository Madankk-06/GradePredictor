import joblib
import pandas as pd
import numpy as np

class GradePredictor:
    def __init__(self):
        print("🔄 Loading models...")
        self.regressor = joblib.load('models/grade_regressor.pkl')
        self.classifier = joblib.load('models/pass_classifier.pkl')
        self.scaler = joblib.load('models/scaler.pkl')
        self.label_encoders = joblib.load('models/label_encoders.pkl')
        self.feature_names = joblib.load('models/feature_names.pkl')
        print("✅ Models loaded successfully!")
    
    def predict(self, student_data):
        """
        student_data: dict or DataFrame with student information
        Returns: prediction results with grade and pass/fail
        """
        if isinstance(student_data, dict):
            student_df = pd.DataFrame([student_data])
        else:
            student_df = student_data.copy()
        
        # Encode categorical variables
        for col, encoder in self.label_encoders.items():
            if col in student_df.columns:
                # Handle unseen categories
                student_df[col] = student_df[col].apply(
                    lambda x: x if x in encoder.classes_ else encoder.classes_[0]
                )
                student_df[col] = encoder.transform(student_df[col])
        
        # Ensure all features are present
        for col in self.feature_names:
            if col not in student_df.columns:
                student_df[col] = 0  # Default value
        
        # Reorder columns
        student_df = student_df[self.feature_names]
        
        # Scale features
        student_scaled = self.scaler.transform(student_df)
        
        # Predict
        predicted_grade = self.regressor.predict(student_scaled)[0]
        pass_probability = self.classifier.predict_proba(student_scaled)[0][1]
        will_pass = self.classifier.predict(student_scaled)[0]
        
        # Clamp grade to 0-20 range
        predicted_grade = max(0, min(20, predicted_grade))
        
        return {
            'predicted_grade': round(predicted_grade, 1),
            'pass_probability': round(pass_probability, 3),
            'will_pass': bool(will_pass),
            'pass_fail_prediction': 'PASS' if will_pass else 'FAIL',
            'confidence': 'High' if pass_probability > 0.8 or pass_probability < 0.2 else 'Medium'
        }

def demo_prediction():
    """Demo with sample student data"""
    predictor = GradePredictor()
    
    print("\n" + "="*60)
    print("🎓 STUDENT GRADE PREDICTION DEMO")
    print("="*60)
    
    # Sample student: Average student with good past grades
    sample_student = {
        'school': 'GP',        # Gabriel Pereira
        'sex': 'F',            # Female
        'age': 17,
        'address': 'U',        # Urban
        'famsize': 'GT3',      # Greater than 3
        'Pstatus': 'T',        # Parents together
        'Medu': 4,             # Mother's education (higher)
        'Fedu': 4,             # Father's education (higher)
        'Mjob': 'teacher',     # Mother's job
        'Fjob': 'services',    # Father's job
        'reason': 'course',    # Reason to choose school
        'guardian': 'mother',  # Guardian
        'traveltime': 1,       # <15 min
        'studytime': 2,        # 2-5 hours/week
        'failures': 0,         # No past failures
        'schoolsup': 'yes',    # Extra educational support
        'famsup': 'no',        # Family educational support
        'paid': 'no',          # Extra paid classes
        'activities': 'yes',   # Extra activities
        'nursery': 'yes',      # Attended nursery
        'higher': 'yes',       # Wants higher education
        'internet': 'yes',     # Internet access
        'romantic': 'no',      # Not in romantic relationship
        'famrel': 4,           # Good family relationship (1-5)
        'freetime': 3,         # Average free time (1-5)
        'goout': 2,            # Go out sometimes (1-5)
        'Dalc': 1,             # Low workday alcohol (1-5)
        'Walc': 1,             # Low weekend alcohol (1-5)
        'health': 5,           # Good health (1-5)
        'absences': 2,         # Few absences
        'G1': 12,              # First period grade (0-20)
        'G2': 13               # Second period grade (0-20)
    }
    
    print("\n📋 Student Profile:")
    print(f"  School: {sample_student['school']}, Age: {sample_student['age']}, Sex: {sample_student['sex']}")
    print(f"  Past Grades: G1={sample_student['G1']}, G2={sample_student['G2']}")
    print(f"  Study Time: {sample_student['studytime']}, Failures: {sample_student['failures']}")
    
    result = predictor.predict(sample_student)
    
    print("\n" + "-"*60)
    print("🔮 PREDICTION RESULTS")
    print("-"*60)
    print(f"📊 Predicted Final Grade (G3):  {result['predicted_grade']}/20")
    print(f"🎯 Pass/Fail Prediction:         {result['pass_fail_prediction']}")
    print(f"📈 Pass Probability:             {result['pass_probability']*100:.1f}%")
    print(f"✅ Confidence Level:             {result['confidence']}")
    print("-"*60)
    
    # Test another student: At-risk student
    print("\n" + "="*60)
    print("🎓 AT-RISK STUDENT DEMO")
    print("="*60)
    
    at_risk_student = {
        'school': 'MS',        # Mousinho da Silveira
        'sex': 'M',
        'age': 19,
        'address': 'R',        # Rural
        'famsize': 'LE3',      # Less than 3
        'Pstatus': 'A',        # Parents apart
        'Medu': 1,             # Low education
        'Fedu': 1,
        'Mjob': 'at_home',
        'Fjob': 'other',
        'reason': 'other',
        'guardian': 'father',
        'traveltime': 4,       # >1 hour
        'studytime': 1,        # <2 hours
        'failures': 2,         # Past failures
        'schoolsup': 'no',
        'famsup': 'no',
        'paid': 'no',
        'activities': 'no',
        'nursery': 'no',
        'higher': 'yes',
        'internet': 'no',
        'romantic': 'yes',
        'famrel': 2,           # Poor family relation
        'freetime': 5,         # Lots of free time
        'goout': 5,            # Go out a lot
        'Dalc': 3,             # Moderate alcohol
        'Walc': 4,             # High weekend alcohol
        'health': 2,           # Poor health
        'absences': 15,        # Many absences
        'G1': 7,               # Poor past grades
        'G2': 6
    }
    
    print("\n📋 Student Profile:")
    print(f"  School: {at_risk_student['school']}, Age: {at_risk_student['age']}, Sex: {at_risk_student['sex']}")
    print(f"  Past Grades: G1={at_risk_student['G1']}, G2={at_risk_student['G2']}")
    print(f"  Study Time: {at_risk_student['studytime']}, Failures: {at_risk_student['failures']}")
    print(f"  Absences: {at_risk_student['absences']}, Health: {at_risk_student['health']}")
    
    result2 = predictor.predict(at_risk_student)
    
    print("\n" + "-"*60)
    print("🔮 PREDICTION RESULTS")
    print("-"*60)
    print(f"📊 Predicted Final Grade (G3):  {result2['predicted_grade']}/20")
    print(f"🎯 Pass/Fail Prediction:         {result2['pass_fail_prediction']}")
    print(f"📈 Pass Probability:             {result2['pass_probability']*100:.1f}%")
    print(f"✅ Confidence Level:             {result2['confidence']}")
    print("-"*60)
    
    return predictor

if __name__ == "__main__":
    predictor = demo_prediction()