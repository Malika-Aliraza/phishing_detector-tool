# Phishing Detection Tool (ML + Rule-Based Hybrid)

This project is a hybrid phishing detection system that uses both rule-based feature extraction and a Machine Learning (Logistic Regression) model to classify URLs as "Phishing" or "Legitimate".

## 🎯 Project Overview
The system extracts key features from a URL (like length, presence of HTTPS, suspicious keywords, etc.) and uses them to:
1.  Calculate a **Rule-Based Risk Score**.
2.  Provide input to a **Machine Learning Model** for a probability score.
3.  Combine both scores for a final **Hybrid Prediction**.

## 📁 Project Structure
- `main.py`: Main CLI execution script.
- `feature_extraction.py`: Module for extracting features from URLs.
- `model.py`: Module for training and loading the ML model.
- `app.py`: Flask web application for a graphical user interface.
- `dataset.csv`: Sample dataset used for training.
- `templates/index.html`: Web UI template for the Flask app.
- `requirements.txt`: List of required Python packages.

## 🚀 How to Run

### 1. In VS Code (Local Machine)
1.  **Install Dependencies**:
    Open your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run CLI Version**:
    ```bash
    python main.py
    ```
3.  **Run Web App Version**:
    ```bash
    python app.py
    ```
    Then open `http://127.0.0.1:5000` in your browser.

### 2. In Google Colab
1.  Upload all project files to your Colab environment.
2.  Install dependencies in a cell:
    ```python
    !pip install flask pandas scikit-learn
    ```
3.  Run the training and CLI:
    ```python
    !python main.py
    ```

## 📊 Explanation for Viva
- **Rule-Based Extraction**: We look for common "red flags" in URLs, such as the absence of HTTPS, use of IP addresses instead of domain names, and suspicious keywords like "login" or "verify".
- **Machine Learning**: We use Logistic Regression because it's efficient for binary classification (Phishing vs. Legitimate) and provides a probability score.
- **Hybrid Approach**: By combining rules and ML, we increase the robustness of the system. Rules catch known patterns, while ML can generalize to new, unseen phishing attempts.
- **Feature Engineering**: Features like URL length and the number of dots are critical because phishing URLs often use long, complex subdomains to mimic legitimate sites.

## 🛡️ Cybersecurity Logic
- **IP Address**: Legitimate sites rarely use raw IP addresses in URLs.
- **HTTPS**: While many phishing sites now use HTTPS, its absence is still a significant risk factor.
- **Special Characters**: Symbols like `@` can be used to redirect users to a different domain than what appears in the URL.
- **Keywords**: Phishing attacks often create a sense of urgency using words like "secure", "update", or "account".
