# accuracy.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from utils import preprocess_negations

def train_and_evaluate_model():
    # Load dataset
    df = pd.read_csv('data/dataset.csv')
    X = df['text'].apply(preprocess_negations)
    y = df['label']

    # Train-test split (80:20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Model training
    model = SVC(probability=True, kernel='linear')
    model.fit(X_train_vec, y_train)

    # Predictions
    y_pred = model.predict(X_test_vec)

    # Evaluation metrics
    print("=== Classification Report ===")
    print(classification_report(y_test, y_pred))

    print("=== Metrics Summary ===")
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"Recall   : {recall_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"F1 Score : {f1_score(y_test, y_pred, average='weighted'):.4f}")

if __name__ == "__main__":
    train_and_evaluate_model()
