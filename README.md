# 🎓 GradePredictor

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

&gt; AI-powered student performance prediction system using Machine Learning

![Demo Screenshot](https://via.placeholder.com/800x400/6366f1/ffffff?text=GradePredictor+Demo)

## 🌟 Features

- 🔮 **Dual Prediction**: Predicts exact grade (0-20) AND pass/fail probability
- 🌐 **Web Interface**: Beautiful, responsive UI built with Flask
- 📊 **ML Models**: Random Forest for high accuracy
- ⚡ **Quick Demo**: 3 preset student profiles for instant testing
- 📱 **Mobile Friendly**: Works on all devices
- 💡 **Smart Insights**: Risk assessment and recommendations

## 🚀 Live Demo

```bash
# Clone repository
git clone https://github.com/Madankk-06/GradePredictor.git
cd GradePredictor

# Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
python api.py

# Open http://127.0.0.1:5000 in browser
