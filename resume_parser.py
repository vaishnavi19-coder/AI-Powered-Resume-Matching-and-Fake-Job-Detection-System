import pdfplumber
import docx
def extract_resume_text(filepath):

    text = ""

    # PDF
    if filepath.lower().endswith(".pdf"):

        with pdfplumber.open(filepath) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

    # DOCX
    elif filepath.lower().endswith(".docx"):

        doc = docx.Document(filepath)

        for para in doc.paragraphs:
            text += para.text + "\n"

    return text.strip()