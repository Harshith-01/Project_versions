from qiskit.circuit.library import ZZFeatureMap
from qiskit_algorithms.utils import algorithm_globals

from qiskit_aer import Aer
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.state_fidelities import ComputeUncompute
from qiskit.primitives import Sampler

from sklearn.svm import SVC
import os, sys, time

# Ensure common and metrics modules are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.preprocessing import load_and_preprocess_data
from metrics.evaluator import evaluate_model, print_metrics


def main():
    start_time = time.time()

    # Load dataset
    X_train, X_test, y_train, y_test = load_and_preprocess_data(
        "data/cardio_train.csv", n_samples=300
    )

    # Set random seed
    algorithm_globals.random_seed = 42

    # Quantum feature map
    feature_map = ZZFeatureMap(feature_dimension=X_train.shape[1], reps=2)

    # Sampler-based fidelity (no backend argument now)
    fidelity = ComputeUncompute(sampler=Sampler())

    # Quantum kernel
    quantum_kernel = FidelityQuantumKernel(fidelity=fidelity, feature_map=feature_map)

    # Train SVM with quantum kernel
    model = SVC(kernel=quantum_kernel.evaluate)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Evaluate performance
    results = evaluate_model(y_test, y_pred)
    print("Quantum SVM Performance:")
    print_metrics(results)

    print(f"Total Execution Time: {time.time() - start_time:.4f} seconds")
    print(f"The sample size is limited to 1000 samples for performance reasons.")


if __name__ == "__main__":
    main()
