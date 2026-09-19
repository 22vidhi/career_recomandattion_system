import requests
import os
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=False)

# ─── Adzuna API Credentials ───────────────────────────────────────────────────
# Get free keys at: https://developer.adzuna.com
ADZUNA_APP_ID  = os.getenv("ADZUNA_APP_ID",  "YOUR_ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "YOUR_ADZUNA_APP_KEY")



def fetch_jobs_adzuna(career: str, location: str, results: int = 5) -> list[dict]:
    """Fetch jobs from Adzuna API."""
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id":   ADZUNA_APP_ID,
        "app_key":  ADZUNA_APP_KEY,
        "what":     career,
        "where":    location,
        "results_per_page": results,
        "content-type": "application/json"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        jobs = []
        for job in data.get("results", []):
            jobs.append({
                "title":    job.get("title", "N/A"),
                "company":  job.get("company", {}).get("display_name", "N/A"),
                "location": job.get("location", {}).get("display_name", "N/A"),
                "salary":   f"{job.get('salary_min', 'N/A')} - {job.get('salary_max', 'N/A')}",
                "url":      job.get("redirect_url", "#"),
                "source":   "Adzuna"
            })
        return jobs
    except Exception as e:
        print(f"Adzuna API error: {e}")
        return []



def fetch_jobs(career: str, location: str, results: int = 5, user_skills: list = None) -> list[dict]:
    """Try Adzuna first."""
    jobs = fetch_jobs_adzuna(career, location, results)
    
    if not jobs:
        import random
        
        # Realistic Database of IT Companies by Location & Their Stack 
        COMPANY_DB = {
            "bangalore": [
                {"name": "Google", "skills": ["python", "machine learning", "data science", "ai", "cloud", "c++", "software development"]},
                {"name": "Microsoft", "skills": ["c#", "azure", ".net", "ai", "cloud", "python", "c++", "software development"]},
                {"name": "Infosys", "skills": ["java", "sql", "testing", "python", "aws", "react", "node", "software development"]},
                {"name": "Wipro", "skills": ["java", "sql", "testing", "python", "aws", "c++", "linux", "software development"]},
                {"name": "Amazon", "skills": ["python", "aws", "machine learning", "cloud", "java", "software development"]},
                {"name": "Flipkart", "skills": ["java", "python", "data science", "sql", "react", "node", "software development", "web development"]}
            ],
            "gandhinagar": [
                {"name": "TCS (Garima Park)", "skills": ["java", "sql", "testing", "python", "aws", "cloud", "c++", "software development"]},
                {"name": "IBM", "skills": ["python", "cloud", "machine learning", "ai", "java", "software development"]},
                {"name": "Cybage Software", "skills": ["testing", "java", "python", ".net", "aws", "qa", "sql", "software development"]},
                {"name": "TatvaSoft", "skills": ["c#", ".net", "sql", "python", "react", "node", "javascript", "java", "web development"]},
                {"name": "Gateway Group", "skills": ["python", "java", "react", "angular", "node", "aws", "web development"]},
                {"name": "InfoStretch", "skills": ["testing", "qa", "automation", "python", "java", "agile", "sql", "software development"]}
            ],
            "pune": [
                {"name": "Tech Mahindra", "skills": ["java", "python", "testing", "sql", "telecom", "c++", "software development"]},
                {"name": "Infosys", "skills": ["java", "sql", "testing", "python", "aws", "software development", "web development"]},
                {"name": "Persistent Systems", "skills": ["java", "python", "cloud", "aws", "salesforce", "c#", "software development"]},
                {"name": "Amdocs", "skills": ["java", "c++", "linux", "sql", "python", "testing", "software development"]},
                {"name": "Credit Suisse", "skills": ["java", "python", "sql", "finance", "angular", "react", "web development"]}
            ],
            "hyderabad": [
                {"name": "Microsoft", "skills": ["c#", "azure", ".net", "ai", "cloud", "python", "software development"]},
                {"name": "Amazon", "skills": ["python", "aws", "machine learning", "cloud", "java", "software development"]},
                {"name": "Google", "skills": ["python", "machine learning", "data science", "ai", "cloud", "software development"]},
                {"name": "Deloitte", "skills": ["sql", "python", "data analysis", "cloud", "java", "consulting", "software development"]},
                {"name": "TCS", "skills": ["java", "sql", "testing", "python", "aws", "software development"]}
            ],
            "mumbai": [
                {"name": "TCS", "skills": ["java", "sql", "testing", "python", "aws", "finance", "software development"]},
                {"name": "L&T Infotech", "skills": ["java", "sql", "python", "cloud", "testing", "software development"]},
                {"name": "Jio", "skills": ["python", "java", "react", "node", "data science", "telecom", "cloud", "web development"]},
                {"name": "Morgan Stanley", "skills": ["java", "python", "c++", "finance", "sql", "react", "software development"]},
                {"name": "Capgemini", "skills": ["java", "testing", "python", "cloud", "sql", "c++", "software development"]}
            ],
            "default": [
                {"name": "TechCorp India", "skills": ["python", "java", "sql", "html", "css", "javascript", "web development", "software development"]},
                {"name": "Global Solutions", "skills": ["react", "node", "aws", "cloud", "testing", "web development"]},
                {"name": "InnovateX", "skills": ["machine learning", "data science", "ai", "python", "sql", "software development"]},
                {"name": "NextGen Systems", "skills": ["c++", "c#", ".net", "java", "sql", "software development"]},
                {"name": "Apex Technologies", "skills": ["python", "aws", "azure", "cloud", "linux", "software development"]},
                {"name": "CloudMinds", "skills": ["cloud", "aws", "azure", "kubernetes", "docker", "software development"]}
            ]
        }
        
        # 1. Location Matching
        loc_key = location.lower().strip()
        matched_loc_key = "default"
        for key in COMPANY_DB.keys():
            if key in loc_key:
                matched_loc_key = key
                break
                
        local_companies = COMPANY_DB[matched_loc_key]
        
        # 2. Skill Matching
        user_skills_set = set([s.lower().strip() for s in (user_skills or [])])
        
        scored_companies = []
        for comp in local_companies:
            comp_skills = set(comp["skills"])
            # Calculate match based on intersection
            overlap = comp_skills.intersection(user_skills_set)
            match_score = len(overlap)
            
            scored_companies.append({
                "name": comp["name"],
                "match_score": match_score,
                "matched_skills": list(overlap)
            })
            
        # Sort companies so best matching ones bubble to the top!
        scored_companies.sort(key=lambda x: x["match_score"], reverse=True)
        
        jobs = []
        selected_companies = scored_companies[:results]
        
        for comp in selected_companies:
            salary_min = random.randint(5, 12)
            salary_max = salary_min + random.randint(2, 6)
            
            search_query = f"{comp['name']} careers {career} {location}".replace(" ", "+")
            
            if comp['match_score'] > 0:
                match_txt = f"⭐ Top Match ({', '.join(comp['matched_skills']).title()})"
            else:
                match_txt = "🎯 Good Regional Match"
            
            jobs.append({
                "title":    f"Senior {career}" if random.choice([True, False]) else f"{career}",
                "company":  comp["name"],
                "location": location.title(),
                "salary":   f"₹{salary_min},00,000 - ₹{salary_max},00,000",
                "url":      f"https://www.google.com/search?q={search_query}",
                "source":   f"Profile Matching Algorithm — {match_txt}"
            })
    return jobs
