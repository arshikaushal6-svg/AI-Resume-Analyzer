import streamlit as st
import pandas as pd
from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_roles, rank_job_roles, analyze_target_role
from roadmap_generator import generate_roadmap

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer & Job Recommendation System")
st.caption("Understand your resume, discover suitable roles, and plan your next learning steps.")
st.info("This tool provides educational guidance only. Match scores are estimates, not hiring decisions.")

@st.cache_data
def get_data():
    return load_skill_dictionary("data/skill_dictionary.csv"), load_job_roles("data/job_roles.csv")

skills_df, roles_df = get_data()

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
if uploaded_file is None:
    st.markdown("### How it works")
    st.markdown("1. Upload a PDF or DOCX resume.\n2. We extract and clean its text.\n3. We identify job-related skills.\n4. We compare your resume with five example job roles.\n5. We show recommendations, skill gaps, and a learning roadmap.")
    st.markdown("**Privacy:** The app processes the uploaded file in memory and does not save the resume to a permanent folder.")
    st.stop()

try:
    raw_text = extract_resume_text(uploaded_file, uploaded_file.name)
except Exception as exc:
    st.error(f"Could not read this file: {exc}")
    st.stop()

if not raw_text.strip():
    st.error("No readable text was found. If this is a scanned PDF, convert it to a text-based PDF or use OCR before uploading.")
    st.stop()

cleaned_text = clean_text(raw_text)
found_skills = extract_skills(cleaned_text, skills_df)
ranked = rank_job_roles(cleaned_text, found_skills, roles_df)

st.success(f"Successfully processed: {uploaded_file.name}")
col1, col2, col3 = st.columns(3)
col1.metric("Skills identified", len(found_skills))
col2.metric("Job roles compared", len(roles_df))
col3.metric("Top recommended role", ranked.iloc[0]["job_role"] if not ranked.empty else "N/A")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Skill analysis", "Role analysis", "Resume text"])
with tab1:
    st.subheader("Your top 3 job recommendations")
    top_three = ranked.head(3)
    for _, row in top_three.iterrows():
        st.write(f"**{row['job_role']}**")
        st.progress(int(row["match_score"]))
        st.write(f"Estimated match: **{row['match_score']:.1f}%**")
        st.divider()
    if found_skills:
        st.write("**Detected skills:** " + ", ".join(found_skills))
    else:
        st.warning("No skills from the current dictionary were detected. Add skills and their common aliases to data/skill_dictionary.csv.")

with tab2:
    st.subheader("Skills found in your resume")
    if found_skills:
        st.write(", ".join(found_skills))
    else:
        st.write("No listed skills detected.")
    st.caption("A missing keyword does not necessarily mean you lack that ability; it may simply be described differently.")
    selected_role = st.selectbox("Choose a target role for skill-gap analysis", roles_df["job_role"].tolist())
    analysis = analyze_target_role(found_skills, roles_df, selected_role)
    left, right = st.columns(2)
    with left:
        st.markdown("**Matched skills**")
        st.write(", ".join(analysis["matched"]) if analysis["matched"] else "None detected")
    with right:
        st.markdown("**Skills to consider learning or adding (if you have them)**")
        st.write(", ".join(analysis["missing"]) if analysis["missing"] else "No gaps detected in this skill list.")
    st.subheader("Suggested learning roadmap")
    roadmap = generate_roadmap(analysis["missing"])
    if roadmap:
        for item in roadmap:
            st.markdown(f"- **{item['week']} — {item['skill']}**: {item['action']}")
    else:
        st.write("No roadmap items are needed for the selected role based on the current skill list.")

with tab3:
    st.subheader("Match scores for all roles")
    chart_data = ranked.set_index("job_role")[["match_score"]]
    st.bar_chart(chart_data)
    st.dataframe(ranked[["job_role", "match_score", "matched_count", "required_count"]], use_container_width=True, hide_index=True)
    st.caption("The score combines TF-IDF cosine similarity (70%) and required-skill coverage (30%). It is an estimate, not a probability of getting a job.")

with tab4:
    st.subheader("Extracted resume text")
    st.text_area("Text extracted from your resume", raw_text, height=350)

# Build a downloadable plain-text analysis report
target = st.session_state.get("report_role", roles_df.iloc[0]["job_role"])
report_role = st.selectbox("Select role for downloadable report", roles_df["job_role"].tolist(), key="report_role")
report_analysis = analyze_target_role(found_skills, roles_df, report_role)
report_roadmap = generate_roadmap(report_analysis["missing"])
report = [
    "AI RESUME ANALYZER - ANALYSIS REPORT",
    f"Resume file: {uploaded_file.name}",
    f"Selected target role: {report_role}",
    "",
    "Detected skills: " + (", ".join(found_skills) if found_skills else "None"),
    "Matched skills: " + (", ".join(report_analysis["matched"]) if report_analysis["matched"] else "None"),
    "Missing keywords to consider: " + (", ".join(report_analysis["missing"]) if report_analysis["missing"] else "None"),
    "",
    "TOP JOB RECOMMENDATIONS:"
]
for _, row in ranked.head(3).iterrows():
    report.append(f"- {row['job_role']}: {row['match_score']:.1f}%")
report += ["", "LEARNING ROADMAP:"]
for item in report_roadmap:
    report.append(f"- {item['week']} — {item['skill']}: {item['action']}")
report += ["", "Note: Scores are estimates for educational guidance, not recruiter decisions."]
st.download_button("⬇️ Download analysis report", "\n".join(report), file_name="resume_analysis_report.txt", mime="text/plain")
