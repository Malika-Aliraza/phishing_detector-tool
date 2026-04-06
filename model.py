import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from feature_extraction import get_feature_list

def train_model(csv_path='dataset.csv', model_path='phishing_model.pkl'):
    """
    Trains a Logistic Regression model on the provided dataset.
    Saves the trained model to a pickle file.
    """
    # Load dataset
    df = pd.read_csv(csv_path)
    
    # Extract features for each URL in the dataset
    X = []
    y = []
    for index, row in df.iterrows():
        features = get_feature_list(row['url'])
        X.append(features)
        y.append(row['label'])
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the model
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Training Accuracy: {accuracy * 100:.2f}%")
    
    # Save the model to a file
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    return model, accuracy

def load_model(model_path='phishing_model.pkl'):
    """
    Loads the trained model from a pickle file.
    """
    try:
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    train_model()
