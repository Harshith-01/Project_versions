import pandas as pd

# Define the cleaned column list
columns = [
    "disease", "symptom_summary", "days",
    # General
    "fever", "fatigue", "weight_loss", "night_sweats", "chills", "loss_of_appetite", "weakness",
    # Respiratory
    "cough", "dry_cough", "productive_cough", "shortness_of_breath", "chest_pain", "wheezing", "sore_throat", "runny_nose", "nasal_congestion",
    # Neurological
    "headache", "dizziness", "confusion", "seizures", "loss_of_consciousness", "insomnia", "blurred_vision", "sensitivity_to_light", "ringing_in_ears",
    # Gastrointestinal
    "nausea", "vomiting", "diarrhea", "constipation", "abdominal_pain", "bloating", "heartburn", "blood_in_stool", "jaundice",
    # Skin / Hair / Nails
    "rash", "itching", "redness", "swelling", "peeling_skin", "dryness", "boils_or_blisters", "hair_loss", "nail_changes",
    # Cardiovascular
    "palpitations", "high_bp", "low_bp", "fainting", "leg_swelling", "visible_veins", "chest_tightness",
    # Urinary / Reproductive
    "painful_urination", "frequent_urination", "urgency_to_urinate", "blood_in_urine", "discharge", "menstrual_irregularity", "pelvic_pain",
    # Endocrine / Metabolic
    "excessive_thirst", "excessive_hunger", "heat_intolerance", "cold_intolerance", "rapid_weight_gain", "slow_healing_wounds",
    # Psychological
    "anxiety", "depression", "irritability", "memory_loss", "mood_swings"
]

# Create empty DataFrame
df = pd.DataFrame(columns=columns)

# Save to CSV
path = "data/disease_symptom_reference_template.csv"
df.to_csv(path, index=False)

path
