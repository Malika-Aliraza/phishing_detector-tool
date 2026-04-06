import os
import pickle
from feature_extraction import extract_features, get_feature_list
from model import train_model

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

def main():
    print("--- Phishing Detection Tool (ML + Rule-Based Hybrid) ---")
    
    # Check if model exists, if not train it
    model_path = 'phishing_model.pkl'
    if not os.path.exists(model_path):
        print("Training model for the first time...")
        model, accuracy = train_model()
        print(f"Model trained with accuracy: {accuracy * 100:.2f}%")
    else:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            print("Loaded pre-trained model.")
    
    while True:
        print("\nEnter a URL to check (or type 'exit' to quit):")
        user_url = input("> ").strip()
        
        if user_url.lower() == 'exit':
            break
        
        if not user_url:
            print("Please enter a valid URL.")
            continue
            
        result = predict_phishing(user_url, model)
        
        print(f"\n--- Prediction Results ---")
        print(f"URL: {result['url']}")
        print(f"Prediction: {result['final_prediction']}")
        print(f"Confidence Score: {result['hybrid_score'] * 100:.2f}%")
        print(f"ML Probability: {result['ml_probability'] * 100:.2f}%")
        print(f"Rule-Based Risk Score: {result['rule_risk_score'] * 100:.2f}%")
        
        print("\n--- Extracted Features ---")
        for key, value in result['features'].items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
