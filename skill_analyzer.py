import re


COMMON_SKILLS = [
    "python","java","c++","sql","flask","django",
    "machine learning","deep learning","nlp",
    "aws","docker","kubernetes",
    "html","css","javascript","react",
    "pandas","numpy","tensorflow","pytorch",
    "api","rest","git","linux","mongodb",
    "rest api","rest apis","api development"
    "mongodb","mysql","scikit-learn",
    "bootstrap","rest api","fastapi","postgresql"
]


def extract_skills(text):
    text = text.lower()
    found = []

    for skill in COMMON_SKILLS:
        if skill.lower() in text.lower():
            found.append(skill)

    return set(found)


def analyze_skill_gap(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    match_ratio = 0
    if len(jd_skills) > 0:
        match_ratio = len(matched) / len(jd_skills) * 100

    return {
        "matched": list(matched),
        "missing": list(missing),
        "match_ratio": round(match_ratio, 2)
    }