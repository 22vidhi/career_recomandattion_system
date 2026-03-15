# 🎯 Career Recommendation System

An intelligent career recommendation platform built with Python and Streamlit.

---

## 🚀 Features
- Resume Upload & Parsing (PDF / DOCX)
- Career Recommendation with Match Score
- Real-Time Job Listings (Adzuna + RapidAPI)
- Resume Generator & Download
- Human-in-the-Loop Feedback System

---

## 📁 Folder Structure
```
career_recommendation_app/
├── app.py
├── .env
├── requirements.txt
├── modules/
│   ├── resume_parser.py
│   ├── career_recommender.py
│   ├── job_fetcher.py
│   ├── resume_generator.py
│   └── feedback_system.py
├── data/
│   └── feedback_log.csv  (auto-created)
└── uploads/resumes/      (auto-created)
```

---

## ⚙️ Installation & Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Add your API keys in `.env`
```
ADZUNA_APP_ID=your_id_here
ADZUNA_APP_KEY=your_key_here
RAPIDAPI_KEY=your_key_here
```

### 3. Run the app
```bash
streamlit run app.py
```

---

## 🔑 API Keys (Both FREE)

| API | Link | Free Tier |
|-----|------|-----------|
| Adzuna | https://developer.adzuna.com | ✅ Yes |
| RapidAPI JSearch | https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch | ✅ Yes |
