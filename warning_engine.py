import re

def detect_warnings(email, title, description):

    text = f"{email} {title} {description}".lower()

    warnings = []

    suspicious_words = [
        "urgent hiring",
        "limited seats",
        "apply immediately",
        "registration fee",
        "payment",
        "earn money fast",
        "work from home",
        "whatsapp",
        "telegram",
        "no interview"
    ]

    for word in suspicious_words:
        if word in text:
            warnings.append(f"Suspicious phrase detected: {word}")

    # suspicious email
    if "gmail.com" in email or "yahoo.com" in email:
        warnings.append("Recruiter using personal email address")

    # unrealistic salary
    salary_patterns = [
        r"\d+\s*lakh",
        r"\d+\s*per month"
    ]

    for pattern in salary_patterns:
        if re.search(pattern, text):
            warnings.append("Unrealistic salary promise detected")

    return warnings