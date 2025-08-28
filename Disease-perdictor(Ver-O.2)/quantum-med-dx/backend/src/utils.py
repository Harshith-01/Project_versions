def frame_to_query(frame: dict) -> str:
    pres = "; ".join(frame.get("present", []))
    abse = "; ".join(frame.get("absent", []))
    return f"present: {pres} | absent: {abse}"

def normalize_probs(diffs):
    total = sum(max(0.0, d["prob"]) for d in diffs) or 1.0
    for d in diffs:
        d["prob"] = max(0.0, d["prob"]) / total
    return diffs
