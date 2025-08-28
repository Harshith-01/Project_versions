import os
import json
import uuid
import pandas as pd
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import StringIO
from typing import Optional

# --- Basic Setup & Configuration ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROCESSED_FILES = {}

# --- Finalized Column List (No Changes) ---
CSV_COLUMNS = [
    'disease', 'symptom_summary', 'gender', 'age_group', 'ethnicity', 'severity_level', 'duration_days',
    'smoking_status', 'alcohol_consumption', 'family_history_of_disease', 'pre_existing_conditions', 'occupation_exposure',
    'heart_rate', 'respiratory_rate', 'body_temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'oxygen_saturation',
    'wbc_count', 'rbc_count', 'platelet_count', 'hemoglobin', 'blood_glucose_level', 'cholesterol_total', 'creatinine',
    'fever', 'fatigue', 'malaise', 'weight_loss', 'night_sweats', 'chills', 'loss_of_appetite', 'weakness', 'lymph_node_swelling',
    'cough', 'dry_cough', 'productive_cough', 'shortness_of_breath', 'chest_pain', 'wheezing',
    'sore_throat', 'runny_nose', 'nasal_congestion', 'headache', 'dizziness', 'ear_pain', 'post_nasal_drip',
    'confusion', 'seizures', 'loss_of_consciousness', 'insomnia', 'memory_loss', 'difficulty_concentrating',
    'blurred_vision', 'sensitivity_to_light', 'ringing_in_ears',
    'nausea', 'vomiting', 'diarrhea', 'constipation', 'abdominal_pain', 'bloating', 'heartburn', 'indigestion', 'blood_in_stool', 'jaundice',
    'rash', 'hives', 'petechiae', 'itching', 'redness', 'swelling', 'peeling_skin', 'dryness', 'boils_or_blisters', 'lesions_or_sores',
    'hair_loss', 'nail_changes',
    'palpitations', 'chest_tightness',
    'muscle_aches', 'joint_pain', 'leg_swelling', 'visible_veins', 'fainting',
    'painful_urination', 'frequent_urination', 'urgency_to_urinate', 'blood_in_urine', 'discharge', 'menstrual_irregularity', 'pelvic_pain',
    'excessive_thirst', 'excessive_hunger', 'heat_intolerance', 'cold_intolerance', 'rapid_weight_gain', 'slow_healing_wounds',
    'anxiety', 'depression', 'irritability', 'mood_swings'
]

# --- Helper and Gemini Functions (No Changes) ---
def scrape_text_from_url(url: str) -> str:
    # ... (function remains the same)
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = [tag.get_text(separator=' ', strip=True) for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])]
        return '\n'.join(texts)
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {e}")

def generate_profiles_with_gemini(disease_name: str, context: str) -> list:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    You are a meticulous medical data scientist with a keen eye for clinical consistency. Based ONLY on the context provided about "{disease_name}", generate 3 distinct hypothetical patient profiles. Each profile must be a valid and logically coherent JSON object.
    Your output MUST be a single valid JSON array of 3 profile objects, with no extra text or markdown.

    Follow these rules precisely for the schema:
    1.  **Patient Narrative Coherence:**
        - **CRITICAL RULE:** The `duration_days` MUST be logically consistent with the `age_group`. The duration of illness cannot be longer than the patient's age. For an 'Adult (30-45)', a duration of 25 years (approx. 9125 days) is plausible, but 40 years is not.
        - For `duration_days` in chronic conditions, provide a realistic number. **Avoid using exact multiples of 365.** Instead, use a number that feels more organic (e.g., for ~10 years, a value like 3642 is better than 3650).
        - For risk factors like `smoking_status` and `alcohol_consumption`, if the context mentions them as general risk factors for the disease, you may infer a plausible status for the profile (e.g., 'Smoker', 'Non-drinker'). If not mentioned at all, continue to use null.

    2.  **Field-Specific Rules:**
        - For `symptom_summary`, provide a concise but detailed clinical summary (2-3 sentences).
        - For Vital Signs and Lab Results, provide a clinically plausible representative numerical value based on the context's descriptions (e.g., "high fever" -> 39.5). If not mentioned or implied, return null.
        - For all symptom fields (e.g., 'fever', 'cough'), return a JSON object with "value" (boolean) and "probability" (float from 0.0 to 1.0).
        - If a symptom is NOT mentioned in the context, assign it a probability of exactly **0.0**.

    The full list of keys to include is: {json.dumps(CSV_COLUMNS)}
    
    Context:
    ---
    {context[:20000]} 
    ---
    """
    try:
        safety_settings = {
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
        }

        response = model.generate_content(
            prompt, 
            generation_config={"temperature": 0.7}, # Slightly increased temperature for more organic values
            safety_settings=safety_settings
        )
        
        raw_text = response.text
        
        start_index = raw_text.find('[')
        if start_index == -1:
            raise ValueError("Could not find the start of a JSON array ('[') in the response.")
            
        end_index = raw_text.rfind(']')
        if end_index == -1:
            raise ValueError("Could not find the end of a JSON array (']') in the response.")

        json_str = raw_text[start_index : end_index + 1]
        
        return json.loads(json_str)

    except Exception as e:
        print("--- Gemini text that failed to parse ---")
        print(raw_text if 'raw_text' in locals() else "Raw text not available.")
        print("------------------------------------------")
        raise HTTPException(status_code=500, detail=f"Error parsing Gemini response: {e}")

@app.post("/process")
async def process_data(
    disease_name: str = Form(...),
    url: str = Form(...),
    # --- CHANGE #1: The file upload is MANDATORY again. Optional logic is removed. ---
    file: UploadFile = File(...)
):
    """
    Processes data and appends it to the content of the MANDATORY uploaded file.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")
    
    # Logic is now simpler: we always read from the provided file.
    df_base = pd.read_csv(file.file)

    scraped_text = scrape_text_from_url(url)
    if not scraped_text:
        raise HTTPException(status_code=400, detail="Could not extract text from the URL.")
    profiles = generate_profiles_with_gemini(disease_name, scraped_text)
    
    new_rows = []
    for profile in profiles:
        row = {col: item['probability'] if isinstance(item := profile.get(col), dict) and 'probability' in item else item for col in CSV_COLUMNS}
        new_rows.append(row)
    df_new = pd.DataFrame(new_rows)
    
    combined_df = pd.concat([df_base, df_new], ignore_index=True)
    
    file_id = str(uuid.uuid4())
    PROCESSED_FILES[file_id] = combined_df.to_csv(index=False)
    
    return {"message": "Processing complete! Click 'Download Result' to get your file.", "file_id": file_id}

@app.get("/download/{file_id}")
async def download_processed_file(file_id: str):
    # ... (function remains the same)
    if file_id not in PROCESSED_FILES:
        raise HTTPException(status_code=404, detail="File not found or has expired.")
    csv_data = PROCESSED_FILES.get(file_id)
    del PROCESSED_FILES[file_id]
    response = StreamingResponse(iter([csv_data]), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=updated_data_{file_id[:8]}.csv"
    return response

# --- CHANGE #2: NEW ENDPOINT TO DOWNLOAD THE BLANK TEMPLATE ---
@app.get("/template")
async def download_template():
    """
    Serves an empty CSV file with only the headers.
    """
    df_template = pd.DataFrame(columns=CSV_COLUMNS)
    
    stream = StringIO()
    df_template.to_csv(stream, index=False)
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=template.csv"
    return response