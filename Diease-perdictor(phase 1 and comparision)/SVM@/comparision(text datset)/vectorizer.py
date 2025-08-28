import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Path to your CSV
csv_path = "data/disease_text_dataset.csv"

# Load CSV
df = pd.read_csv(csv_path)

# Assuming your CSV has a 'text' column — change if different
text_column = "text"

if text_column not in df.columns:
    raise ValueError(f"'{text_column}' column not found in CSV. Found columns: {df.columns.tolist()}")

texts = df[text_column].astype(str).tolist()

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Fit the vectorizer
vectorizer.fit(texts)

# Get all features (vocabulary words)
feature_names = vectorizer.get_feature_names_out()

# Print total count and all features
print(f"Total features: {len(feature_names)}\n")
print("=== Vocabulary ===")
for feature in feature_names:
    print(feature,end=", ")
