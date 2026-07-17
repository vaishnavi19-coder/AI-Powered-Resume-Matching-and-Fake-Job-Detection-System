def generate_feedback(resume, skill_data):

    missing = skill_data.get("missing", [])

    feedback = []

    resume_lower = resume.lower()

    # ---------------- MISSING SKILLS ----------------
    if missing:
        feedback.append(
            "Add missing skills from the job description like: "
            + ", ".join(missing[:5])
        )
    else:
        feedback.append(
            "Excellent skill alignment with the job description."
        )

    # ---------------- PROJECTS ----------------
    if "project" not in resume_lower:
        feedback.append(
            "Add project section with technical projects."
        )

    # ---------------- EXPERIENCE ----------------
    if "experience" not in resume_lower:
        feedback.append(
            "Add internship or practical experience section."
        )

    # ---------------- CERTIFICATIONS ----------------
    if "certification" not in resume_lower:
        feedback.append(
            "Adding certifications can improve resume strength."
        )

    # ---------------- GITHUB ----------------
    if "github" not in resume_lower:
        feedback.append(
            "Add GitHub profile link for project visibility."
        )

    # ---------------- LINKEDIN ----------------
    if "linkedin" not in resume_lower:
        feedback.append(
            "Add LinkedIn profile for professional presence."
        )

    # ---------------- ACHIEVEMENTS ----------------
    if "achievement" not in resume_lower:
        feedback.append(
            "Mention achievements, hackathons, or competitions."
        )

    return feedback