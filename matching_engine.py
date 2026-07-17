import pandas as pd
import numpy as np
import os
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- MODEL ----------------
model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------------- DATA ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
jobs_path = os.path.join(BASE_DIR,"dataset", "jobs.csv")

jobs_df = pd.read_csv(jobs_path)

jobs_df["title"] = jobs_df["title"].astype(str)

# CLEAN TITLES
jobs_df["title"] = jobs_df["title"].apply(lambda x: " ".join(x.split()[:3]))
jobs_df["title"] = jobs_df["title"].str.replace(r"\s+", " ", regex=True).str.strip()

# ---------------- CLEAN TEXT ----------------
def clean(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9+.# ]", " ", text)
    return text


# ---------------- SKILL DATABASE ----------------
SKILL_DB = [
    "python","java","c++","sql","machine learning","deep learning",
    "flask","django","html","css","javascript","react","node",
    "pandas","numpy","tensorflow","keras","nlp","api","git","mongodb",
    "mysql","scikit-learn","bootstrap","rest api","fastapi",
    "postgresql"
]


def extract_skills(text):
    text = text.lower()
    return list({skill for skill in SKILL_DB if skill in text})


# ---------------- SKILL SCORE ----------------
def skill_score(resume, jd):

    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(jd)

    if not jd_skills:
        return 0

    match = len(set(resume_skills) & set(jd_skills))
    return (match / len(jd_skills)) * 100


# ---------------- KEYWORD SCORE ----------------
def keyword_score(resume, jd):

    stopwords = {
    "the","and","for","with","this","that","you",
    "our","your","are","have","has","will","from",
    "job","work","team","using","required"
    }

    resume_words = {
    w for w in clean(resume).split()
    if len(w) > 2 and w not in stopwords
    }

    jd_words = {
    w for w in clean(jd).split()
    if len(w) > 2 and w not in stopwords
    }

    if not jd_words:
        return 0

    match = len(resume_words & jd_words)
    return (match / len(jd_words)) * 100


# ---------------- SEMANTIC SCORE ----------------
def semantic_score(resume, jd):

    vectors = model.encode([resume, jd])

    sim = cosine_similarity([vectors[0]], [vectors[1]])[0][0]

    return max(0, (sim + 1) / 2 * 100)


# ---------------- FINAL SCORE ----------------
def calculate_similarity(resume, jd):
    sem = semantic_score(resume, jd)
    skill = skill_score(resume, jd)
    keyword = keyword_score(resume, jd)
    final = (0.35 * sem) + (0.4 * skill) + (0.25 * keyword)

    # IMPORTANT PENALTY
    if skill < 10:
        final *= 0.75

    elif skill < 25:
        final *= 0.9
    return round(final, 2)

# ---------------- JOB VECTORS ----------------
job_vectors = model.encode(
    jobs_df["title"].tolist(),
    show_progress_bar=True
)


# ---------------- JOB MATCHING ----------------
def get_top_job_matches(resume_text):

    resume_vector = model.encode([resume_text])
    scores = cosine_similarity(resume_vector, job_vectors)[0]

    top_indices = np.argsort(scores)[::-1][:5]

    results = []

    for i in top_indices:

        title = str(jobs_df.iloc[i]["title"])
        title = " ".join(title.split()[:3])

        results.append({
            "title": title,
            "match": round(float(scores[i]) * 100, 2)
        })

    return results