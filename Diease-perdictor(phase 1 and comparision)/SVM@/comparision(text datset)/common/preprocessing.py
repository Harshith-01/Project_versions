import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def handle_negations(text):
    # Simple negation handler (you can expand this with NLP techniques)
    text = re.sub(r"\bno (\w+)", r"no_\1", text)
    text = re.sub(r"\bnot (\w+)", r"no_\1", text)
    text = re.sub(r"\bwithout (\w+)", r"no_\1", text)
    return text

def load_and_preprocess_data(filepath, n_samples=1000):
    df = pd.read_csv(filepath, header=None, names=["label", "text"])
    df = df.dropna().head(n_samples)

    df["text"] = df["text"].str.lower().apply(handle_negations)
    X = df["text"]
    y = df["label"]

    vectorizer = TfidfVectorizer()
    X_vectorized = vectorizer.fit_transform(X)

    return train_test_split(X_vectorized, y, test_size=0.2, random_state=42)
