# /backend/app/services/quantum_service.py
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

class QuantumService:
    def sample_question(self, weights: list) -> int:
        """
        Selects an index based on a list of weights using a quantum circuit.
        """
        num_questions = len(weights)
        if num_questions == 0:
            return -1 # No questions to sample
        if num_questions == 1:
            return 0 # Only one choice

        # Normalize weights to probabilities
        probabilities = np.array(weights) / np.sum(weights)
        
        # Calculate rotation angles based on probabilities
        # This maps probabilities to angles for Ry gates
        angles = [2 * np.arcsin(np.sqrt(p)) for p in probabilities]

        # Determine the number of qubits needed
        num_qubits = int(np.ceil(np.log2(num_questions)))

        # Create a quantum circuit
        qc = QuantumCircuit(num_qubits)

        # Apply rotations - a simple amplitude encoding scheme
        # Note: This is a heuristic. More complex state preparation algorithms exist.
        # For simplicity, we apply rotations to each qubit.
        for i in range(min(num_qubits, len(angles))):
            qc.ry(angles[i], i)

        qc.measure_all()

        # Use the Aer simulator
        simulator = AerSimulator()
        compiled_circuit = transpile(qc, simulator)
        result = simulator.run(compiled_circuit, shots=1024).result()
        counts = result.get_counts(qc)

        # Find the most frequent outcome that is a valid index
        valid_counts = {int(k, 2): v for k, v in counts.items() if int(k, 2) < num_questions}
        if not valid_counts:
            # Fallback to classical if quantum sampling yields no valid indices (rare)
            return np.random.choice(len(weights), p=probabilities)

        # Return the index with the highest count
        chosen_index = max(valid_counts, key=valid_counts.get)
        
        return chosen_index