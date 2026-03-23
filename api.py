from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
import os

# Get the directory where api.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add src to path
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from predict import GradePredictor

app = Flask(__name__, 
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
CORS(app)

# Change working directory so models load correctly
os.chdir(BASE_DIR)

# Initialize predictor
print("🔄 Loading models...")
predictor = GradePredictor()
print("✅ API Ready!")
# Initialize predictor
print("🔄 Loading models...")
predictor = GradePredictor()
print("✅ API Ready!")

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        
        # Convert to proper types
        student_data = {
            'school': data.get('school', 'GP'),
            'sex': data.get('sex', 'F'),
            'age': int(data.get('age', 17)),
            'address': data.get('address', 'U'),
            'famsize': data.get('famsize', 'GT3'),
            'Pstatus': data.get('Pstatus', 'T'),
            'Medu': int(data.get('Medu', 2)),
            'Fedu': int(data.get('Fedu', 2)),
            'Mjob': data.get('Mjob', 'services'),
            'Fjob': data.get('Fjob', 'services'),
            'reason': data.get('reason', 'course'),
            'guardian': data.get('guardian', 'mother'),
            'traveltime': int(data.get('traveltime', 1)),
            'studytime': int(data.get('studytime', 2)),
            'failures': int(data.get('failures', 0)),
            'schoolsup': data.get('schoolsup', 'no'),
            'famsup': data.get('famsup', 'yes'),
            'paid': data.get('paid', 'no'),
            'activities': data.get('activities', 'yes'),
            'nursery': data.get('nursery', 'yes'),
            'higher': data.get('higher', 'yes'),
            'internet': data.get('internet', 'yes'),
            'romantic': data.get('romantic', 'no'),
            'famrel': int(data.get('famrel', 4)),
            'freetime': int(data.get('freetime', 3)),
            'goout': int(data.get('goout', 2)),
            'Dalc': int(data.get('Dalc', 1)),
            'Walc': int(data.get('Walc', 1)),
            'health': int(data.get('health', 4)),
            'absences': int(data.get('absences', 2)),
            'G1': int(data.get('G1', 12)),
            'G2': int(data.get('G2', 13))
        }
        
        # Make prediction
        result = predictor.predict(student_data)
        
        # Add risk level
        if result['pass_probability'] < 0.3:
            risk_level = 'High Risk'
            advice = 'Immediate intervention recommended. Increase study time, reduce absences, seek tutoring.'
        elif result['pass_probability'] < 0.7:
            risk_level = 'Medium Risk'
            advice = 'Monitor closely. Consider additional support and study plan.'
        else:
            risk_level = 'Low Risk'
            advice = 'On track. Maintain current performance.'
        
        response = {
            'success': True,
            'prediction': {
                'predicted_grade': result['predicted_grade'],
                'max_grade': 20,
                'pass_fail': result['pass_fail_prediction'],
                'pass_probability': result['pass_probability'],
                'confidence': result['confidence'],
                'risk_level': risk_level,
                'advice': advice
            },
            'input_summary': {
                'past_grades': f"G1={student_data['G1']}, G2={student_data['G2']}",
                'study_time': f"{student_data['studytime']} ({['<2hrs', '2-5hrs', '5-10hrs', '>10hrs'][student_data['studytime']-1]})",
                'absences': student_data['absences'],
                'failures': student_data['failures']
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/demo', methods=['GET'])
def demo():
    """Get demo student profiles"""
    demos = {
        'high_achiever': {
            'name': 'High Achiever',
            'data': {'school':'GP','sex':'F','age':17,'address':'U','famsize':'GT3','Pstatus':'T','Medu':4,'Fedu':4,'Mjob':'teacher','Fjob':'teacher','reason':'course','guardian':'mother','traveltime':1,'studytime':4,'failures':0,'schoolsup':'no','famsup':'yes','paid':'yes','activities':'yes','nursery':'yes','higher':'yes','internet':'yes','romantic':'no','famrel':5,'freetime':2,'goout':1,'Dalc':1,'Walc':1,'health':5,'absences':0,'G1':18,'G2':19}
        },
        'average_student': {
            'name': 'Average Student',
            'data': {'school':'GP','sex':'M','age':16,'address':'U','famsize':'LE3','Pstatus':'T','Medu':2,'Fedu':2,'Mjob':'services','Fjob':'services','reason':'home','guardian':'father','traveltime':2,'studytime':2,'failures':0,'schoolsup':'no','famsup':'no','paid':'no','activities':'yes','nursery':'yes','higher':'yes','internet':'yes','romantic':'no','famrel':4,'freetime':3,'goout':3,'Dalc':1,'Walc':2,'health':4,'absences':4,'G1':11,'G2':12}
        },
        'at_risk': {
            'name': 'At-Risk Student',
            'data': {'school':'MS','sex':'M','age':18,'address':'R','famsize':'GT3','Pstatus':'A','Medu':1,'Fedu':1,'Mjob':'at_home','Fjob':'other','reason':'other','guardian':'father','traveltime':4,'studytime':1,'failures':2,'schoolsup':'no','famsup':'no','paid':'no','activities':'no','nursery':'no','higher':'yes','internet':'no','romantic':'yes','famrel':2,'freetime':5,'goout':5,'Dalc':4,'Walc':5,'health':2,'absences':20,'G1':6,'G2':5}
        }
    }
    return jsonify(demos)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'models_loaded': True})

if __name__ == '__main__':
    print("🚀 Starting GradePredictor API...")
    print("📍 Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)