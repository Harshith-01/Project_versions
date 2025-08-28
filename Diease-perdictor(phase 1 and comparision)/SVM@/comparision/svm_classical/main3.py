import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from xgboost import XGBClassifier
from common.preprocessing import load_and_preprocess_data
from metrics.evaluator import evaluate_model, print_metrics

def main():
    start_time = time.time()

    X_train, X_test, y_train, y_test = load_and_preprocess_data(
        "data/cardio_train.csv", 
        n_samples=None
    )

    # Tuned XGBoost model
    clf = XGBClassifier(
        n_estimators=300,
        learning_rate=0.1,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=0.1,
        reg_lambda=1,
        random_state=42,
        n_jobs=-1,
        eval_metric="logloss"
    )

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    results = evaluate_model(y_test, y_pred)
    print("\nClassical XGBoost Performance:")
    print_metrics(results)

    end_time = time.time()
    print(f"\nTotal Execution Time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    print("Starting script...")
    main()

