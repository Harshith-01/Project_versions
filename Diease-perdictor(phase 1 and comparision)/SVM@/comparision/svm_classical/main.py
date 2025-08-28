import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from common.preprocessing import load_and_preprocess_data
from metrics.evaluator import evaluate_model, print_metrics

def main():
    start_time = time.time()

    X_train, X_test, y_train, y_test = load_and_preprocess_data(
        "data/cardio_train.csv", 
        n_samples=None
    )

    # Parameter tuning for better performance
    param_grid = {
        "C": [0.1, 1, 10],
        "gamma": ["scale", 0.01, 0.001],
        "kernel": ["rbf", "poly"]
    }
    grid = GridSearchCV(SVC(), param_grid, cv=3, scoring="f1", n_jobs=-1, verbose=1)
    grid.fit(X_train, y_train)

    best_clf = grid.best_estimator_
    y_pred = best_clf.predict(X_test)

    results = evaluate_model(y_test, y_pred)
    print("\nClassical SVM Performance:")
    print(f"Best Parameters: {grid.best_params_}")
    print_metrics(results)

    end_time = time.time()
    print(f"\nTotal Execution Time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
