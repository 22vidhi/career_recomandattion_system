import pdfplumber
import docx
import re
import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    "python", "java", "c++", "c#", "javascript", "typescript", "sql", "r", "matlab",
    "machine learning", "deep learning", "nlp", "data analysis", "data science",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
    "html", "css", "react", "angular", "vue", "node.js", "django", "flask", "fastapi",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "linux",
    "excel", "power bi", "tableau", "hadoop", "spark", "mongodb", "mysql", "postgresql",
    "project management", "agile", "scrum", "communication", "teamwork", "leadership",
    "photoshop", "illustrator", "figma", "ui/ux", "autocad", "solidworks",
    "networking", "cybersecurity", "penetration testing", "cloud computing",
    "devops", "ci/cd", "rest api", "microservices", "blockchain", "iot"
]

EDUCATION_KEYWORDS = [
    "b.tech", "b.e", "bsc", "b.sc", "msc", "m.sc", "mba", "m.tech", "m.e",
    "phd", "ph.d", "bachelor", "master", "diploma", "10th", "12th",
    "computer science", "information technology", "electronics", "mechanical",
    "civil", "electrical", "chemical", "biotechnology", "data science"
]


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    return ""


def extract_skills(text):
    text_lower = text.lower()
    found_skills = [skill for skill in SKILL_KEYWORDS if skill in text_lower]
    return list(set(found_skills))


def extract_education(text):
    text_lower = text.lower()
    found_edu = [edu for edu in EDUCATION_KEYWORDS if edu in text_lower]
    return list(set(found_edu))


def extract_experience_years(text):
    matches = re.findall(r'(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)', text.lower())
    if matches:
        return max(int(m[0]) for m in matches)
    return 0


def parse_resume(file_path):
    text = extract_text(file_path)
    return {
        "raw_text": text,
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience_years": extract_experience_years(text)
    }
