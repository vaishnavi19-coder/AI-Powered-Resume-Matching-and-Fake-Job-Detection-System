from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from flask import session
from resume_parser import extract_resume_text
from matching_engine import calculate_similarity, get_top_job_matches
from scam_model import predict_scam
from skill_analyzer import analyze_skill_gap
from feedback_engine import generate_feedback
from skill_extractor import extract_skills
from warning_engine import detect_warnings

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- PROCESS RESUME ----------------
@app.route("/process", methods=["POST"])
def process():
    resume_text = request.form.get("resume_text", "").strip()
    uploaded_file = request.files.get("resume_file")

    final_resume = ""

    if uploaded_file and uploaded_file.filename != "":
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
        uploaded_file.save(filepath)
        final_resume = extract_resume_text(filepath)

    elif resume_text:
        final_resume = resume_text

    else:
        return redirect(url_for("index"))

    return render_template("upload_jd.html", resume=final_resume)


# ---------------- ANALYZE ----------------
@app.route("/analyze", methods=["POST"])
def analyze():
    resume = request.form.get("resume", "").strip()
    jd = request.form.get("jd_text", "").strip()

    if not resume or not jd:
        return "Missing resume or job description", 400

    match_score = calculate_similarity(resume, jd)
    jobs = get_top_job_matches(resume)
    skills = extract_skills(resume)

    skill_data = analyze_skill_gap(resume, jd)
    if not isinstance(skill_data, dict):
        skill_data = {"matched": [], "missing": [], "match_ratio": 0}

    feedback = generate_feedback(resume, skill_data)

    return render_template(
        "result.html",
        match_score=match_score,
        jobs=jobs,
        skills=skills,
        resume=resume,
        jd=jd,
        skill_data=skill_data,
        feedback=feedback
    )


# ---------------- SCAM CHECKER ----------------
@app.route("/scam-checker")
def scam_checker():
    return render_template("scam_checker.html")


@app.route("/analyze-scam", methods=["POST"])
def analyze_scam():
    email = request.form.get("email", "")
    title = request.form.get("title", "")
    description = request.form.get("description", "")

    score, label = predict_scam(email, title, description)
    warnings = detect_warnings(email, title, description)

    return render_template(
        "scam_result.html",
        result=label,
        score=score,
        warnings=warnings
    )

# ---------------- DOWNLOAD REPORT ----------------
@app.route("/download-report", methods=["POST"])
def download_report():
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from flask import send_file, request

    pdf_path = "report.pdf"
    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    elements = []

    resume = request.form.get("resume", "")
    jd = request.form.get("jd_text", "")
    match_score = request.form.get("match_score", 0)

    elements.append(Paragraph("JobShield AI Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"<b>Match Score:</b> {match_score}%", styles["BodyText"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Resume Preview:</b>", styles["Heading2"]))
    elements.append(Paragraph(resume[:1000], styles["BodyText"]))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Job Description Preview:</b>", styles["Heading2"]))
    elements.append(Paragraph(jd[:1000], styles["BodyText"]))

    doc.build(elements)

    return send_file(pdf_path, as_attachment=True)


# ---------------- RUN ----------------
if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(host="0.0.0.0", port=7860)
    
    
