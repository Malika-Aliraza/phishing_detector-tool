import os
import pickle
from flask import Flask, render_template, request, jsonify
from feature_extraction import extract_features, get_feature_list
from model import train_model

app = Flask(__name__)

# Load or train the model
model_path = 'phishing_model.pkl'
if not os.path.exists(model_path):
    print("Training model for the first time...")
    model, accuracy = train_model()
else:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

def predict_phishing(url, model):
    """
    Predicts if a URL is phishing or legitimate using a hybrid approach.
    Combines rule-based features and ML model predictions.
    """
    # Extract rule-based features and risk score
    features = extract_features(url)
    rule_risk_score = features['rule_risk_score']
    
    # Extract features for the ML model
    ml_features = [get_feature_list(url)]
    
    # Get ML model prediction and probability
    ml_prediction = model.predict(ml_features)[0]
    ml_probability = model.predict_proba(ml_features)[0][1]
    
    # Hybrid Score Calculation (Simple Average)
    # 0.5 weight for ML, 0.5 weight for Rule-Based
    hybrid_score = (ml_probability + rule_risk_score) / 2
    
    # Final Classification
    final_prediction = "Phishing" if hybrid_score >= 0.5 else "Legitimate"
    
    return {
        'url': url,
        'final_prediction': final_prediction,
        'hybrid_score': hybrid_score,
        'ml_probability': ml_probability,
        'rule_risk_score': rule_risk_score,
        'features': features
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form.get('url')
    if not url:
        return render_template('index.html', error='Please enter a URL.')
    
    result = predict_phishing(url, model)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
