# backend/main.py

import os
import pandas as pd

# Finalized CSV_COLUMNS list
CSV_COLUMNS = [
    # Demographics & Metadata
    'disease', 'symptom_summary', 'gender', 'age_group', 'ethnicity', 'severity_level', 'duration_days',
    
    # Risk Factors & Patient History
    'smoking_status', 'alcohol_consumption', 'family_history_of_disease', 'pre_existing_conditions', 'occupation_exposure',
    
    # Vital Signs
    'heart_rate', 'respiratory_rate', 'body_temperature',
    'blood_pressure_systolic', 'blood_pressure_diastolic', 'oxygen_saturation',
    
    # Common Lab Results
    'wbc_count', 'rbc_count', 'platelet_count', 'hemoglobin',
    'blood_glucose_level', 'cholesterol_total', 'creatinine',

    # General Systemic Symptoms
    'fever', 'fatigue', 'malaise', 'weight_loss', 'night_sweats',
    'chills', 'loss_of_appetite', 'weakness', 'lymph_node_swelling',
    
    # Respiratory Symptoms
    'cough', 'dry_cough', 'productive_cough',
    'shortness_of_breath', 'chest_pain', 'wheezing',
    
    # HEENT (Head, Eyes, Ears, Nose, Throat)
    'sore_throat', 'runny_nose', 'nasal_congestion',
    'headache', 'dizziness', 'ear_pain', 'post_nasal_drip',
    
    # Neurological Symptoms
    'confusion', 'seizures', 'loss_of_consciousness',
    'insomnia', 'memory_loss', 'difficulty_concentrating',
    
    # Vision & Hearing
    'blurred_vision', 'sensitivity_to_light', 'ringing_in_ears',
    
    # Gastrointestinal Symptoms
    'nausea', 'vomiting', 'diarrhea', 'constipation', 'abdominal_pain',
    'bloating', 'heartburn', 'indigestion', 'blood_in_stool', 'jaundice',
    
    # Skin (Integumentary) Symptoms
    'rash', 'hives', 'petechiae', 'itching', 'redness',
    'swelling', 'peeling_skin', 'dryness', 'boils_or_blisters', 'lesions_or_sores',
    
    # Hair & Nails
    'hair_loss', 'nail_changes',
    
    # Cardiovascular Symptoms
    'palpitations', 'chest_tightness',
    
    # Musculoskeletal Symptoms
    'muscle_aches', 'joint_pain', 'leg_swelling',
    'visible_veins', 'fainting',
    
    # Genitourinary Symptoms
    'painful_urination', 'frequent_urination', 'urgency_to_urinate',
    'blood_in_urine', 'discharge', 'menstrual_irregularity', 'pelvic_pain',
    
    # Endocrine/Metabolic Symptoms
    'excessive_thirst', 'excessive_hunger', 'heat_intolerance',
    'cold_intolerance', 'rapid_weight_gain', 'slow_healing_wounds',
    
    # Psychological Symptoms
    'anxiety', 'depression', 'irritability', 'mood_swings'
]

def generate_template_csv(output_path="data/disease_symptom_reference_template.csv"):
    """Generate an empty CSV template with finalized medical dataset columns."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(columns=CSV_COLUMNS)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    path = generate_template_csv()
    print(f"Template CSV created at: {path}")
