import math
import numpy as np
from typing import List
from config import settings

# ---------- classical sampling ----------
def classical_sample(weights: List[float]) -> int:
    w = np.array(weights, dtype=float)
    w = w / (w.sum() if w.sum() > 0 else 1.0)
    return int(np.random.choice(len(w), p=w))

# ---------- quantum sampling (Qiskit Aer) ----------
def quantum_sample(weights: List[float]) -> int:
    # Map weights -> rotations (superposition over choices)
    try:
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator
        from qiskit.transpiler import PassManager
    except Exception:
        # fallback
        return classical_sample(weights)

    k = len(weights)
    n = max(1, math.ceil(math.log2(k)))
    # normalize
    w = np.array(weights, dtype=float)
    w = w / (w.sum() if w.sum() > 0 else 1.0)

    # simple amplitude-style mapping:
    # For each qubit, set Ry angle proportional to entropy-weighted mean
    entropy = -np.sum(w * np.log(w + 1e-9))
    angles = [(0.5 + 0.5*entropy/np.log(k)) * np.pi] * n

    qc = QuantumCircuit(n, n)
    for i, ang in enumerate(angles):
        qc.ry(ang, i)
    qc.barrier()
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    compiled = PassManager().run(qc)
    job = sim.run(compiled, shots=2048)
    counts = job.result().get_counts()

    # map bitstrings -> indices
    def b2i(bits): return int(bits.replace(" ", "") , 2)
    # sample proportional to counts but ignore out-of-range
    items = []
    probs = []
    total = 0
    for b, c in counts.items():
        idx = b2i(b)
        if idx < k:
            items.append(idx)
            probs.append(c)
            total += c
    if not items:
        return classical_sample(weights)
    probs = np.array(probs, dtype=float) / total
    return int(np.random.choice(items, p=probs))

def pick_followup(candidates: List[dict], diffs: List[dict], quantum_mode: bool):
    # Heuristic score per question: cover top-3 diffs, prefer rule-in/out over 'clarify', de-duplicate
    top3 = {d["name"] for d in sorted(diffs, key=lambda x: x["prob"], reverse=True)[:3]}
    scores = []
    seen = set()
    cleaned = []
    for c in candidates:
        q = c.get("question","").strip()
        if not q or q in seen:
            continue
        seen.add(q)
        sig = c.get("expected_signal","clarify")
        base = 0.6 if sig!="clarify" else 0.4
        # tiny diversity bonus
        sc = base + 0.05*len(q.split())
        scores.append(sc)
        cleaned.append(c)
    if not cleaned:
        return None, "skipped"
    if quantum_mode and settings.QUANTUM_FOLLOWUPS:
        idx = quantum_sample(scores)
        mode = "quantum"
    else:
        idx = classical_sample(scores)
        mode = "classical"
    return cleaned[idx]["question"], mode
