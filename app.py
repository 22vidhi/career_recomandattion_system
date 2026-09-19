import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=False)

from modules.resume_parser     import parse_resume
from modules.career_recommender import recommend_careers
from modules.job_fetcher        import fetch_jobs
from modules.resume_generator   import generate_resume
from modules.feedback_system    import save_feedback, get_feedback_summary

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Career Recommendation System",
    page_icon="🎯",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1F497D;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .career-card {
        background: linear-gradient(135deg, #f0f4ff, #e8f0fe);
        border-left: 5px solid #1F497D;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #333333;
    }
    .job-card {
        background: #f9f9f9;
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
        color: #333333;
    }
    .score-badge {
        background-color: #1F497D;
        color: white;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🎯 Career Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload your resume & get personalized career guidance with real-time job listings</div>', unsafe_allow_html=True)
st.divider()

# ── Sidebar: User Profile ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("👤 User Profile")
    full_name    = st.text_input("Full Name",         placeholder="e.g. Rahul Sharma")
    education    = st.text_input("Education",          placeholder="e.g. B.Tech Computer Science")
    skills_input = st.text_input("Skills (comma separated)", placeholder="e.g. python, sql, machine learning")
    interests    = st.text_input("Interests",          placeholder="e.g. AI, web development")
    pref_field   = st.text_input("Preferred Field",    placeholder="e.g. Data Science")
    pref_role    = st.text_input("Preferred Job Role", placeholder="e.g. Data Analyst")
    pref_loc     = st.text_input("Preferred Location", placeholder="e.g. Bangalore")
    email        = st.text_input("Email",              placeholder="e.g. rahul@email.com")
    phone        = st.text_input("Phone",              placeholder="e.g. +91 9876543210")

    st.divider()
    st.subheader("📊 Feedback Summary")
    summary = get_feedback_summary()
    col1, col2, col3 = st.columns(3)
    col1.metric("👍 Helpful",     summary["Helpful"])
    col2.metric("👎 Not Helpful", summary["Not Helpful"])
    col3.metric("🔧 Needs Work",  summary["Needs Improvement"])

# ── Main Tabs ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📄 Resume Upload", "🎯 Career Recommendations", "💼 Job Listings", "📝 Resume Generator"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — Resume Upload
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.subheader("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

    parsed_data = {}

    if uploaded_file:
        suffix = ".pdf" if uploaded_file.name.endswith(".pdf") else ".docx"
        # Save original file so we can edit it later
        os.makedirs("uploads/resumes", exist_ok=True)
        permanent_path = os.path.join("uploads", "resumes", f"latest_upload{suffix}")
        
        with open(permanent_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state["uploaded_resume_path"] = permanent_path

        with st.spinner("Parsing resume..."):
            parsed_data = parse_resume(permanent_path)

        st.success("✅ Resume parsed successfully!")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📚 Extracted Skills:**")
            if parsed_data["skills"]:
                for s in parsed_data["skills"]:
                    st.markdown(f"- {s.title()}")
            else:
                st.info("No standard skills detected.")
        with col2:
            st.markdown("**🎓 Education Detected:**")
            if parsed_data["education"]:
                for e in parsed_data["education"]:
                    st.markdown(f"- {e.title()}")
            else:
                st.info("No standard education keywords detected.")

        st.markdown(f"**🏢 Experience:** {parsed_data['experience_years']} year(s)")

        # Merge profile skills with resume skills
        profile_skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()] if skills_input else []
        all_skills = list(set(parsed_data["skills"] + profile_skills))
        st.session_state["all_skills"]   = all_skills
        st.session_state["parsed_data"]  = parsed_data
        st.session_state["full_name"]    = full_name
        st.session_state["education"]    = education
        st.session_state["interests"]    = interests
        st.session_state["pref_loc"]     = pref_loc
        st.session_state["email"]        = email
        st.session_state["phone"]        = phone

    elif skills_input:
        profile_skills = [s.strip().lower() for s in skills_input.split(",") if s.strip()]
        st.session_state["all_skills"] = profile_skills
        st.info("ℹ️ No resume uploaded. Using manually entered skills.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — Career Recommendations
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.subheader("🎯 Career Recommendations")

    if "all_skills" not in st.session_state or not st.session_state["all_skills"]:
        st.warning("⚠️ Please upload your resume or enter skills in the sidebar first.")
    else:
        user_skills = st.session_state["all_skills"]
        st.markdown(f"**Skills used for matching:** {', '.join(s.title() for s in user_skills)}")

        with st.spinner("Generating recommendations..."):
            recommendations = recommend_careers(user_skills, top_n=5)

        st.session_state["recommendations"] = recommendations

        for i, rec in enumerate(recommendations):
            with st.container():
                st.markdown(f"""
                <div class="career-card">
                    <h4>#{i+1} {rec['career']}
                    <span class="score-badge">Match: {rec['match_score']}%</span></h4>
                    <p>{rec['description']}</p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("✅ **Matched Skills:**")
                    st.write(", ".join(s.title() for s in rec["matched_skills"]) or "None")
                with col2:
                    st.markdown("❌ **Missing Skills:**")
                    st.write(", ".join(s.title() for s in rec["missing_skills"]) or "None")

                # Feedback
                feedback = st.radio(
                    f"Was this recommendation helpful?",
                    ["Helpful", "Not Helpful", "Needs Improvement"],
                    key=f"feedback_{i}",
                    horizontal=True
                )
                if st.button(f"Submit Feedback", key=f"fb_btn_{i}"):
                    save_feedback(
                        user_name=full_name or "Anonymous",
                        recommended_career=rec["career"],
                        match_score=rec["match_score"],
                        feedback=feedback
                    )
                    st.success("✅ Feedback submitted!")
                st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — Job Listings
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.subheader("💼 Real-Time Job Listings")

    search_career  = st.text_input("Job Title / Career",  value=pref_role or "Data Scientist")
    search_location = st.text_input("Location",            value=pref_loc  or "Bangalore")

    if st.button("🔍 Search Jobs"):
        with st.spinner(f"Fetching jobs for {search_career} in {search_location}..."):
            user_skills = st.session_state.get("all_skills", [])
            jobs = fetch_jobs(search_career, search_location, results=6, user_skills=user_skills)

        if jobs:
            unique_companies = len(set(job['company'] for job in jobs))
            st.success(f"Found {len(jobs)} customized job(s) from {unique_companies} companies matching your profile in {search_location}!")
            for job in jobs:
                st.markdown(f"""
                <div class="job-card">
                    <b>🏢 {job['title']}</b> at <b>{job['company']}</b><br>
                    📍 {job['location']} &nbsp;|&nbsp; 💰 {job['salary']}<br>
                    🔗 <a href="{job['url']}" target="_blank">Apply Now</a>
                    &nbsp;&nbsp;<small>({job['source']})</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No jobs found. Try different keywords or location.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4 — Resume Generator
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.subheader("📝 Generate Improved Resume")

    if "recommendations" not in st.session_state:
        st.warning("⚠️ Please get career recommendations first (Tab 2).")
    else:
        recs = st.session_state["recommendations"]
        top  = recs[0]

        st.info(f"📌 Generating resume optimized for: **{top['career']}**")

        if st.button("⚙️ Generate Resume"):
            user_data = {
                "name":       st.session_state.get("full_name", full_name) or "Your Name",
                "email":      st.session_state.get("email", email)         or "",
                "phone":      st.session_state.get("phone", phone)         or "",
                "location":   st.session_state.get("pref_loc", pref_loc)   or "",
                "education":  [st.session_state.get("education", education) or "Not Provided"],
                "skills":     st.session_state.get("all_skills", []),
                "experience": f"{st.session_state.get('parsed_data', {}).get('experience_years', 0)} year(s)",
                "interests":  st.session_state.get("interests", interests)  or ""
            }

            output_path = "uploads/resumes/improved_resume.docx"
            os.makedirs("uploads/resumes", exist_ok=True)

            original_path = st.session_state.get("uploaded_resume_path")
            with st.spinner("Modifying your resume..."):
                path = generate_resume(
                    user_data=user_data,
                    recommended_career=top["career"],
                    missing_skills=top["missing_skills"],
                    output_path=output_path,
                    original_path=original_path
                )

            st.success("✅ Resume generated successfully!")
            with open(path, "rb") as f:
                st.download_button(
                    label="⬇️ Download Improved Resume (.docx)",
                    data=f,
                    file_name="improved_resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
