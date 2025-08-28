# svm_classical/main.py
import os, sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.svm import SVC
from common.preprocessing import load_and_preprocess_data
from metrics.evaluator import compute_extended_metrics, print_metrics

def main():
    start_total = time.time()
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(out_dir, exist_ok=True)

    X_train, X_test, y_train, y_test = load_and_preprocess_data("data/disease_text_dataset.csv", n_samples=1000)

    clf = SVC(kernel="rbf", C=1.0, gamma="scale")
    t0 = time.time()
    clf.fit(X_train, y_train)
    train_time = time.time() - t0

    t1 = time.time()
    y_pred = clf.predict(X_test)
    predict_time = time.time() - t1

    total_time = time.time() - start_total

    # Try to get decision/probability scores for AUC plotting
    y_score = None
    try:
        if hasattr(clf, "predict_proba"):
            y_score = clf.predict_proba(X_test)
        elif hasattr(clf, "decision_function"):
            y_score = clf.decision_function(X_test)
    except Exception:
        y_score = None

    results = compute_extended_metrics(y_test, y_pred, y_score=y_score)
    results["y_true_raw"] = y_test
    results["train_time_sec"] = train_time
    results["predict_time_sec"] = predict_time
    results["total_time_sec"] = total_time

    print_metrics(results, title="Classical SVM Performance", save_dir=out_dir, y_score=y_score)

    print("Timing (seconds):")
    print(f" Training time : {train_time:.2f}s")
    print(f" Predict time  : {predict_time:.2f}s")
    print(f" Total runtime : {total_time:.2f}s")

if __name__ == "__main__":
    main()
