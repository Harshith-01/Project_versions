# svm_quantum/main.py
import os 
import sys
import time
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.algorithms.classifiers import QSVC

from common.preprocessing import load_and_preprocess_data
from metrics.evaluator import compute_extended_metrics, print_metrics

def get_top_terms_for_pca(pca, data_csv_path, top_k=8):
    """
    Fit a TF-IDF (simple) on the raw corpus and map PCA components back to top terms.
    This gives an interpretable idea of which TF-IDF terms contribute most to each PCA feature.
    """
    df = pd.read_csv(data_csv_path, header=None, names=["label", "text"])
    texts = df["text"].dropna().astype(str).str.lower()

    # simple negation handling to match preprocessing (if you had more complex, adjust accordingly)
    texts = texts.str.replace(r"\bno (\w+)", r"no_\1", regex=True)
    texts = texts.str.replace(r"\bnot (\w+)", r"no_\1", regex=True)
    texts = texts.str.replace(r"\bwithout (\w+)", r"no_\1", regex=True)

    vectorizer = TfidfVectorizer(stop_words="english", max_features=20000)
    X_all = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()

    components = pca.components_  # shape (n_components, n_original_features)
    top_terms = []
    for i, comp in enumerate(components):
        idxs = np.argsort(np.abs(comp))[::-1][:top_k]
        terms = [feature_names[idx] for idx in idxs]
        top_terms.append(terms)
    return top_terms

def main():
    start_total = time.time()
    out_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    os.makedirs(out_dir, exist_ok=True)

    # Load and preprocess data (returns sparse TF-IDF matrices)
    X_train, X_test, y_train, y_test = load_and_preprocess_data("data/disease_text_dataset.csv", n_samples=1000)

    # Convert to dense and reduce to small dimension for quantum processing
    X_train_dense = X_train.toarray()
    X_test_dense = X_test.toarray()

    pca_components = 4
    pca = PCA(n_components=pca_components)
    X_train_reduced = pca.fit_transform(X_train_dense)
    X_test_reduced = pca.transform(X_test_dense)

    # Print which TF-IDF terms contributed to each PCA component
    try:
        top_terms = get_top_terms_for_pca(pca, "data/disease_text_dataset.csv", top_k=8)
        print("PCA -> Top contributing TF-IDF terms per reduced feature (component):")
        for i, terms in enumerate(top_terms):
            print(f" Component {i+1}: {', '.join(terms)}")
    except Exception as e:
        print("Could not extract PCA top terms:", e)

    # Quantum feature map (unchanged)
    feature_map = ZZFeatureMap(feature_dimension=pca_components, reps=2, entanglement="full")

    # Fidelity-based Quantum Kernel (unchanged)
    quantum_kernel = FidelityQuantumKernel(feature_map=feature_map)

    # Quantum SVM classifier (unchanged)
    qsvc = QSVC(quantum_kernel=quantum_kernel)

    # Measure training & predict times
    t0 = time.time()
    qsvc.fit(X_train_reduced, y_train)
    train_time = time.time() - t0

    t1 = time.time()
    y_pred = qsvc.predict(X_test_reduced)
    predict_time = time.time() - t1

    total_time = time.time() - start_total

    # Compute basic + extended metrics
    # Try to obtain score for AUC plotting: prefer predict_proba else decision_function
    y_score = None
    try:
        if hasattr(qsvc, "predict_proba"):
            y_score = qsvc.predict_proba(X_test_reduced)
        elif hasattr(qsvc, "decision_function"):
            y_score = qsvc.decision_function(X_test_reduced)
    except Exception:
        y_score = None

    results = compute_extended_metrics(y_test, y_pred, y_score=y_score)
    # include raw y_true for ROC plotting convenience
    results["y_true_raw"] = y_test
    # add timing info
    results["train_time_sec"] = train_time
    results["predict_time_sec"] = predict_time
    results["total_time_sec"] = total_time

    # Print metrics and save confusion/ROC plots to outputs folder
    print_metrics(results, title="Quantum SVM Performance", save_dir=out_dir, y_score=y_score)

    # Print timing summary
    print("Timing (seconds):")
    print(f" Training time : {train_time:.2f}s")
    print(f" Predict time  : {predict_time:.2f}s")
    print(f" Total runtime : {total_time:.2f}s")

if __name__ == "__main__":
    main()
