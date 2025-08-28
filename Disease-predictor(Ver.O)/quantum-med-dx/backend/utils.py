import re
import uuid
import numpy as np
from typing import Dict, List

NEGATIONS = ["no", "without", "denies", "not", "absence of"]

def generate_id() -> str:
    return str(uuid.uuid4())

def normalize_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())

def extract_negations(text: str) -> Dict[str, List[str]]:
    # Simple heuristic: capture tokens after negation words up to punctuation
    present, absent = set(), set()
    t = normalize_text(text)
    tokens = re.split(r"[,.!?;]", t)
    for seg in tokens:
        seg = seg.strip()
        if any(neg in seg.split() for neg in NEGATIONS):
            # naive extraction: take nouns/words after negation marker
            words = [w for w in re.findall(r"[a-zA-Z\-]+", seg)]
            idx = next((i for i,w in enumerate(words) if w in NEGATIONS), None)
            if idx is not None:
                for w in words[idx+1:]:
                    if len(w) > 2:
                        absent.add(w)
        else:
            for w in re.findall(r"[a-zA-Z\-]+", seg):
                if len(w) > 2:
                    present.add(w)
    # Remove collisions
    present = {w for w in present if w not in absent}
    return {"present": sorted(list(present)), "absent": sorted(list(absent))}

def frame_to_query(frame: Dict) -> str:
    present = "; ".join(frame.get("present", []))
    absent = "; ".join(f"no {x}" for x in frame.get("absent", []))
    duration = frame.get("duration_days")
    parts = []
    if duration:
        parts.append(f"duration {duration} days")
    if present:
        parts.append(present)
    if absent:
        parts.append(absent)
    return " ; ".join(parts)

def softmax(xs: List[float]) -> List[float]:
    a = np.array(xs, dtype=float)
    a = a - np.max(a)
    e = np.exp(a)
    s = e / (e.sum() + 1e-9)
    return s.tolist()

def choose_classical(weights: List[float]) -> int:
    w = np.array(weights, dtype=float)
    w = w / (w.sum() + 1e-9)
    return int(np.random.choice(len(w), p=w))
