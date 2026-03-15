import csv
import os
from datetime import datetime

FEEDBACK_FILE = "data/feedback_log.csv"
FIELDNAMES = ["timestamp", "user_name", "recommended_career", "match_score", "feedback"]


def save_feedback(user_name: str, recommended_career: str, match_score: float, feedback: str):
    """Save user feedback to CSV file."""
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(FEEDBACK_FILE)

    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp":           datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_name":           user_name,
            "recommended_career":  recommended_career,
            "match_score":         match_score,
            "feedback":            feedback
        })


def load_feedback() -> list[dict]:
    """Load all feedback records."""
    if not os.path.isfile(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_feedback_summary() -> dict:
    """Return count of each feedback type."""
    records = load_feedback()
    summary = {"Helpful": 0, "Not Helpful": 0, "Needs Improvement": 0}
    for r in records:
        fb = r.get("feedback", "")
        if fb in summary:
            summary[fb] += 1
    return summary
