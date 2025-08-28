from typing import List
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit_aer.backends import AerSimulator

# Tiny quantum sampler: map weights -> rotation angles -> measure
def quantum_sample(weights: List[float], shots: int = 1024) -> int:
    w = np.array(weights, dtype=float)
    w = w / (w.sum() + 1e-9)
    n = len(w)
    # Use enough qubits to represent n states (ceil log2 n)
    qubits = int(np.ceil(np.log2(max(2, n))))
    dim = 2 ** qubits

    # Pad weights to power of 2
    if dim > n:
        w = np.pad(w, (0, dim - n), mode='constant', constant_values=0.0)

    # Prepare amplitudes roughly proportional to sqrt(prob)
    amps = np.sqrt(w)
    amps = amps / (np.linalg.norm(amps) + 1e-12)

    # Simple state-prep via Ry ladder for demo (not exact general prep)
    qc = QuantumCircuit(qubits)
    # Start with uniform superposition
    for q in range(qubits):
        qc.h(q)
    # Encode bias toward lower indices via Ry on first qubit as a toy mechanism
    bias = float(np.clip(np.sum(np.arange(dim) * w) / (dim-1 + 1e-9), 0.0, 1.0))
    theta = (bias * np.pi)
    qc.ry(theta, 0)
    qc.measure_all()

    backend = AerSimulator(method='automatic')
    job = backend.run(qc, shots=shots)
    counts = job.result().get_counts()

    # Convert bitstrings to index
    def b2i(bits: str) -> int:
        return int(bits.replace(" ", "")[::-1], 2)  # Qiskit bit order
    # Aggregate probabilities
    probs = np.zeros(dim)
    for bstr, c in counts.items():
        probs[b2i(bstr)] += c
    probs = probs / probs.sum()

    # pick index by max prob (argmax) to keep deterministic per run; or sample again:
    idx = int(np.argmax(probs))
    # If idx >= n (padded), fall back to most probable in range
    if idx >= n:
        idx = int(np.argmax(probs[:n]))
    return idx
