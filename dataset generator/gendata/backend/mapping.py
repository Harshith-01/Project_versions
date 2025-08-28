import re
from typing import Optional
from .config import COLUMNS

# Common synonyms -> canonical names
SYMPTOM_SYNONYMS = {
    "haematuria": "blood_in_urine",
    "hematuria": "blood_in_urine",
    "polyuria": "frequent_urination",
    "dysuria": "painful_urination",
    "dyspnea": "shortness_of_breath",
    "dyspnoea": "shortness_of_breath",
    "pyrexia": "fever",
    "pruritus": "itching",
    "dermatitis": "rash",
    "hemoptysis": "productive_cough",
    "syncope": "fainting",
    "palpitation": "palpitations",
    "joint swelling": "swelling",
    "urticaria": "rash",
}

# canonical symptoms start after first 9 columns
CANONICAL_SYMPTOMS = set(COLUMNS[9:])

def to_canonical(symptom_name: str) -> Optional[str]:
    s = symptom_name.strip().lower()
    s = re.sub(r"[^a-z0-9_ ]+", "", s)
    s = s.replace(" ", "_")
    s = SYMPTOM_SYNONYMS.get(s, s)
    return s if s in CANONICAL_SYMPTOMS else None
