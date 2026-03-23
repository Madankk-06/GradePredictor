#!/usr/bin/env python3
"""
GradePredictor - Student Performance Prediction System
Run this for interactive predictions!
"""

import sys
import os
sys.path.insert(0, 'src')

from predict import GradePredictor
import pandas as pd

def interactive_mode():
    """Interactive CLI for making predictions"""
    print("="*70)
    print("🎓 GRADEPREDICTOR - Student Grade Prediction System")
    print("="*70)
    print("\nLoading AI models...")
    
    try:
        predictor = GradePredictor()
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        print("Please run: python src/train_model.py")
        return
    
    print("\n✅ Ready! Enter student details (or type 'demo' for examples, 'quit' to exit)")
    
    while True:
        print("\n" + "-"*70)
        command = input("\nEnter command (predict/demo/quit): ").strip().lower()
        
        if command == 'quit':
            print("👋 Goodbye!")
            break
            
        elif command == 'demo':
            run_demos(predictor)
            
        elif command == 'predict':
            student = get_student_input()
            result = predictor.predict(student)
            display_result(result)
            
        else:
            print("Unknown command. Use: predict, demo, or quit")

def get_student_input():
    """Get student data from user input"""
    print("\n📋 Enter student information:")
    
    student = {}
    
    # Required fields with examples
    fields = {
        'school': ('GP/MS', 'GP'),
        'sex': ('F/M', 'F'),
        'age': ('15-22', '17'),
        'address': ('U/R', 'U'),
        'famsize': ('GT3/LE3', 'GT3'),
        'Pstatus': ('T/A', 'T'),
        'Medu': ('0-4', '4'),
        'Fedu': ('0-4', '4'),
        'Mjob': ('teacher/health/services/at_home/other', 'teacher'),
        'Fjob': ('teacher/health/services/at_home/other', 'services'),
        'reason': ('home/reputation/course/other', 'course'),
        'guardian': ('mother/father/other', 'mother'),
        'traveltime': ('1-4', '1'),
        'studytime': ('1-4', '2'),
        'failures': ('0-4', '0'),
        'schoolsup': ('yes/no', 'yes'),
        'famsup': ('yes/no', 'no'),
        'paid': ('yes/no', 'no'),
        'activities': ('yes/no', 'yes'),
        'nursery': ('yes/no', 'yes'),
        'higher': ('yes/no', 'yes'),
        'internet': ('yes/no', 'yes'),
        'romantic': ('yes/no', 'no'),
        'famrel': ('1-5', '4'),
        'freetime': ('1-5', '3'),
        'goout': ('1-5', '2'),
        'Dalc': ('1-5', '1'),
        'Walc': ('1-5', '1'),
        'health': ('1-5', '5'),
        'absences': ('0-93', '2'),
        'G1': ('0-20', '12'),
        'G2': ('0-20', '13')
    }
    
    for field, (options, default) in fields.items():
        value = input(f"  {field} [{options}] (default: {default}): ").strip()
        student[field] = value if value else default
        
        # Convert numeric fields
        if field in ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
                     'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2']:
            student[field] = int(student[field])
    
    return student

def display_result(result):
    """Display prediction result"""
    print("\n" + "="*70)
    print("🔮 PREDICTION RESULTS")
    print("="*70)
    print(f"📊 Predicted Final Grade:        {result['predicted_grade']}/20")
    print(f"🎯 Pass/Fail Prediction:         {result['pass_fail_prediction']}")
    print(f"📈 Pass Probability:             {result['pass_probability']*100:.1f}%")
    print(f"✅ Confidence:                   {result['confidence']}")
    print("="*70)
    
    # Advice
    if result['will_pass']:
        if result['pass_probability'] > 0.9:
            print("💡 Status: Excellent standing! Keep it up!")
        else:
            print("💡 Status: On track to pass. Consider improving study habits.")
    else:
        print("⚠️  ALERT: At risk of failing! Recommend:")
        print("   - Increase study time")
        print("   - Reduce absences")
        print("   - Seek tutoring support")

def run_demos(predictor):
    """Run demo predictions"""
    print("\n" + "="*70)
    print("🎓 RUNNING DEMO PREDICTIONS")
    print("="*70)
    
    demos = [
        {
            'name': '⭐ High Achiever',
            'data': {'school':'GP','sex':'F','age':17,'address':'U','famsize':'GT3','Pstatus':'T','Medu':4,'Fedu':4,'Mjob':'teacher','Fjob':'teacher','reason':'course','guardian':'mother','traveltime':1,'studytime':4,'failures':0,'schoolsup':'no','famsup':'yes','paid':'yes','activities':'yes','nursery':'yes','higher':'yes','internet':'yes','romantic':'no','famrel':5,'freetime':2,'goout':1,'Dalc':1,'Walc':1,'health':5,'absences':0,'G1':18,'G2':19}
        },
        {
            'name': '📚 Average Student', 
            'data': {'school':'GP','sex':'M','age':16,'address':'U','famsize':'LE3','Pstatus':'T','Medu':2,'Fedu':2,'Mjob':'services','Fjob':'services','reason':'home','guardian':'father','traveltime':2,'studytime':2,'failures':0,'schoolsup':'no','famsup':'no','paid':'no','activities':'yes','nursery':'yes','higher':'yes','internet':'yes','romantic':'no','famrel':4,'freetime':3,'goout':3,'Dalc':1,'Walc':2,'health':4,'absences':4,'G1':11,'G2':12}
        },
        {
            'name': '⚠️  At-Risk Student',
            'data': {'school':'MS','sex':'M','age':18,'address':'R','famsize':'GT3','Pstatus':'A','Medu':1,'Fedu':1,'Mjob':'at_home','Fjob':'other','reason':'other','guardian':'father','traveltime':4,'studytime':1,'failures':2,'schoolsup':'no','famsup':'no','paid':'no','activities':'no','nursery':'no','higher':'yes','internet':'no','romantic':'yes','famrel':2,'freetime':5,'goout':5,'Dalc':4,'Walc':5,'health':2,'absences':20,'G1':6,'G2':5}
        }
    ]
    
    for demo in demos:
        print(f"\n{'='*70}")
        print(f"👤 {demo['name']}")
        print(f"Past Grades: G1={demo['data']['G1']}, G2={demo['data']['G2']}")
        print(f"Study Time: {demo['data']['studytime']}, Absences: {demo['data']['absences']}")
        
        result = predictor.predict(demo['data'])
        display_result(result)

def quick_predict(G1, G2, studytime=2, failures=0, absences=2):
    """Quick prediction with minimal inputs (others use defaults)"""
    predictor = GradePredictor()
    
    # Default student profile
    student = {
        'school': 'GP', 'sex': 'F', 'age': 17, 'address': 'U', 'famsize': 'GT3',
        'Pstatus': 'T', 'Medu': 2, 'Fedu': 2, 'Mjob': 'services', 'Fjob': 'services',
        'reason': 'course', 'guardian': 'mother', 'traveltime': 1, 'studytime': studytime,
        'failures': failures, 'schoolsup': 'no', 'famsup': 'yes', 'paid': 'no',
        'activities': 'yes', 'nursery': 'yes', 'higher': 'yes', 'internet': 'yes',
        'romantic': 'no', 'famrel': 4, 'freetime': 3, 'goout': 2, 'Dalc': 1,
        'Walc': 1, 'health': 4, 'absences': absences, 'G1': G1, 'G2': G2
    }
    
    return predictor.predict(student)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        # Quick demo mode
        predictor = GradePredictor()
        run_demos(predictor)
    else:
        interactive_mode()