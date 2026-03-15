from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

CAREER_PROFILES = {
    "Data Scientist": {
        "skills": ["python", "machine learning", "deep learning", "pandas", "numpy",
                   "scikit-learn", "tensorflow", "data analysis", "sql", "nlp"],
        "description": "Analyzes complex data to derive insights using ML models and statistical techniques."
    },
    "Software Engineer": {
        "skills": ["python", "java", "c++", "javascript", "git", "rest api",
                   "docker", "sql", "agile", "microservices"],
        "description": "Designs and develops software applications and systems."
    },
    "Web Developer": {
        "skills": ["html", "css", "javascript", "react", "node.js", "angular",
                   "vue", "git", "rest api", "sql"],
        "description": "Builds and maintains websites and web applications."
    },
    "DevOps Engineer": {
        "skills": ["docker", "kubernetes", "aws", "azure", "gcp", "linux",
                   "ci/cd", "git", "devops", "networking"],
        "description": "Manages infrastructure, deployment pipelines, and cloud services."
    },
    "Cybersecurity Analyst": {
        "skills": ["cybersecurity", "networking", "penetration testing", "linux",
                   "python", "aws", "cloud computing", "git"],
        "description": "Protects systems and networks from cyber threats and vulnerabilities."
    },
    "UI/UX Designer": {
        "skills": ["figma", "photoshop", "illustrator", "ui/ux", "html", "css",
                   "communication", "teamwork"],
        "description": "Designs intuitive and visually appealing user interfaces."
    },
    "Data Analyst": {
        "skills": ["sql", "excel", "python", "power bi", "tableau", "data analysis",
                   "pandas", "numpy", "communication"],
        "description": "Interprets data and generates reports to support business decisions."
    },
    "Machine Learning Engineer": {
        "skills": ["python", "tensorflow", "pytorch", "keras", "scikit-learn",
                   "machine learning", "deep learning", "docker", "aws", "sql"],
        "description": "Develops and deploys machine learning models at scale."
    },
    "Cloud Engineer": {
        "skills": ["aws", "azure", "gcp", "docker", "kubernetes", "linux",
                   "devops", "networking", "ci/cd", "python"],
        "description": "Designs and manages scalable cloud infrastructure and services."
    },
    "Project Manager": {
        "skills": ["project management", "agile", "scrum", "communication",
                   "leadership", "teamwork", "excel"],
        "description": "Plans and oversees projects to ensure on-time and on-budget delivery."
    }
}


def calculate_match_score(user_skills, career_skills):
    matched = set(user_skills) & set(career_skills)
    if not career_skills:
        return 0
    return round((len(matched) / len(career_skills)) * 100, 2)


def recommend_careers(user_skills, top_n=5):
    scores = []
    for career, profile in CAREER_PROFILES.items():
        score = calculate_match_score(user_skills, profile["skills"])
        matched = list(set(user_skills) & set(profile["skills"]))
        missing = list(set(profile["skills"]) - set(user_skills))
        scores.append({
            "career": career,
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "description": profile["description"]
        })
    scores.sort(key=lambda x: x["match_score"], reverse=True)
    return scores[:top_n]
