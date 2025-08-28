import re

NEG_WORDS = r"(?:no|not|without|denies|denied|absence of|negative for)"
def parse_symptoms(text: str, checkbox: list[str] | None = None):
    # naive tokenization
    tokens = re.findall(r"[a-zA-Z]+(?:[- ][a-zA-Z]+)?", text.lower())
    base = set(checkbox or [])
    present, absent = set(), set()
    # toy lexicon (expand as you like)
    vocab = {"fever","cough","headache","chills","sore throat","nausea","vomiting","diarrhea","rash","fatigue","chest pain","shortness of breath"}
    s = text.lower()
    for sym in vocab:
        # patterns
        if re.search(fr"{NEG_WORDS}\s+{re.escape(sym)}", s):
            absent.add(sym)
        elif re.search(fr"{re.escape(sym)}", s):
            present.add(sym)
    present |= base
    return {"present": sorted(present - absent), "absent": sorted(absent)}
