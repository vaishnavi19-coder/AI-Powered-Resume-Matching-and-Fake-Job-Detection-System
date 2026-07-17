import re


SKILLS = [

    "python",
    "java",
    "c++",
    "sql",
    "mysql",
    "mongodb",
    "machine learning",
    "deep learning",
    "data analysis",
    "flask",
    "django",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "nlp",
    "tensorflow",
    "pandas",
    "numpy",
    "excel",
    "power bi",
    "tableau",
    "communication",
    "teamwork",
    "problem solving"

]


def extract_skills(resume_text):

    resume_text = resume_text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, resume_text):

            found_skills.append(skill.title())

    return found_skills