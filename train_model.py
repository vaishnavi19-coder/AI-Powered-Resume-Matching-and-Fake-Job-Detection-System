import pandas as pd
import re
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# ---------------- PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "fake_job_postings.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_DIR, exist_ok=True)

# ---------------- LOAD ----------------
df = pd.read_csv(DATA_PATH)

# ---------------- CLEAN (IMPROVED) ----------------
def clean(text):
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text

df["text"] = (
    df["title"].fillna("") + " " +
    df["description"].fillna("") + " " +
    df["location"].fillna("") + " " +
    df["company_profile"].fillna("") + " " +
    df["requirements"].fillna("")
)
df["text"] = df["text"].apply(clean)

X = df["text"]
y = df["fraudulent"]

# ---------------- SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- PIPELINE (IMPORTANT UPGRADE) ----------------
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=8000,
        ngram_range=(1, 2),   # BIG IMPROVEMENT
        stop_words="english"
    )),
    ("clf", LogisticRegression(
    max_iter=2000,
    class_weight="balanced"
))
])

# ---------------- TRAIN ----------------
pipeline.fit(X_train, y_train)

# ---------------- EVALUATE ----------------
y_pred = pipeline.predict(X_test)
print("\nMODEL REPORT:\n")
print(classification_report(y_test, y_pred))

# ---------------- SAVE ONLY PIPELINE ----------------
with open(os.path.join(MODEL_DIR, "scam_model.pkl"), "wb") as f:
    pickle.dump(pipeline, f)

print("\nModel trained and saved successfully!")