from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # if empty, fallback extractor used
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")
DATASET_CSV = os.getenv("DATASET_CSV", "../data/disease_symptom_reference.csv")
PORT = int(os.getenv("PORT", "8000"))

# Columns: meta + provenance + canonical symptoms
COLUMNS = [
    "disease","symptom_summary","gender","age_group","severity_level","duration_days",
    "source_url","retrieved_at","model_version",
    "fever","fatigue","weight_loss","night_sweats","chills","loss_of_appetite","weakness",
    "cough","dry_cough","productive_cough","shortness_of_breath","chest_pain","wheezing","sore_throat","runny_nose","nasal_congestion",
    "headache","dizziness","confusion","seizures","loss_of_consciousness","insomnia","blurred_vision","sensitivity_to_light","ringing_in_ears",
    "nausea","vomiting","diarrhea","constipation","abdominal_pain","bloating","heartburn","blood_in_stool","jaundice",
    "rash","itching","redness","swelling","peeling_skin","dryness","boils_or_blisters","hair_loss","nail_changes",
    "palpitations","high_bp","low_bp","fainting","leg_swelling","visible_veins","chest_tightness",
    "painful_urination","frequent_urination","urgency_to_urinate","blood_in_urine","discharge","menstrual_irregularity","pelvic_pain",
    "excessive_thirst","excessive_hunger","heat_intolerance","cold_intolerance","rapid_weight_gain","slow_healing_wounds",
    "anxiety","depression","irritability","memory_loss","mood_swings"
]

GENDER_VALUES = ["male","female","other","all"]
AGE_GROUP_VALUES = ["child","adolescent","adult","elderly","all"]
SEVERITY_VALUES = ["mild","moderate","severe","critical","unspecified"]
