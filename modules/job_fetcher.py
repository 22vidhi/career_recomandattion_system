import requests
import os

# ─── Adzuna API Credentials ───────────────────────────────────────────────────
# Get free keys at: https://developer.adzuna.com
ADZUNA_APP_ID  = os.getenv("ADZUNA_APP_ID",  "YOUR_ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "YOUR_ADZUNA_APP_KEY")

# ─── RapidAPI Credentials ─────────────────────────────────────────────────────
# Get free keys at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
RAPIDAPI_KEY  = os.getenv("RAPIDAPI_KEY", "YOUR_RAPIDAPI_KEY")
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"


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


def fetch_jobs_rapidapi(career: str, location: str, results: int = 5) -> list[dict]:
    """Fetch jobs from RapidAPI JSearch."""
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key":  RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "query":      f"{career} in {location}",
        "page":       "1",
        "num_pages":  "1"
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        jobs = []
        for job in data.get("data", [])[:results]:
            jobs.append({
                "title":    job.get("job_title", "N/A"),
                "company":  job.get("employer_name", "N/A"),
                "location": job.get("job_city", "N/A") + ", " + job.get("job_country", ""),
                "salary":   f"{job.get('job_min_salary', 'N/A')} - {job.get('job_max_salary', 'N/A')}",
                "url":      job.get("job_apply_link", "#"),
                "source":   "RapidAPI"
            })
        return jobs
    except Exception as e:
        print(f"RapidAPI error: {e}")
        return []


def fetch_jobs(career: str, location: str, results: int = 5) -> list[dict]:
    """Try Adzuna first, fall back to RapidAPI."""
    jobs = fetch_jobs_adzuna(career, location, results)
    if not jobs:
        jobs = fetch_jobs_rapidapi(career, location, results)
    if not jobs:
        # Demo fallback so UI never breaks
        jobs = [
            {
                "title":    f"{career} Engineer",
                "company":  "TechCorp India",
                "location": location,
                "salary":   "₹6,00,000 - ₹12,00,000",
                "url":      "https://www.naukri.com",
                "source":   "Demo"
            }
        ]
    return jobs
