import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.svm import SVC
from common.preprocessing import load_and_preprocess_data
from metrics.evaluator import evaluate_model, print_metrics

def main():
    start_time = time.time()

    X_train, X_test, y_train, y_test = load_and_preprocess_data(
        "data/cardio_train.csv", 
        n_samples=None
    )

    # Single SVM with fixed parameters
    clf = SVC(C=10, gamma='scale', kernel='rbf')  # you can tweak these if needed
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    results = evaluate_model(y_test, y_pred)
    print("\nClassical SVM Performance:")
    print_metrics(results)

    end_time = time.time()
    print(f"\nTotal Execution Time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
