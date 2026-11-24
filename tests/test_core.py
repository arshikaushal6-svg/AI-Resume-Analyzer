import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_roles, rank_job_roles, analyze_target_role

def test_clean_and_extract():
    cleaned = clean_text("I use Python, C++ and SQL.")
    skills = load_skill_dictionary("data/skill_dictionary.csv")
    found = extract_skills(cleaned, skills)
    assert "Python" in found
    assert "C++" in found
    assert "SQL" in found

def test_role_ranking_and_gaps():
    roles = load_job_roles("data/job_roles.csv")
    resume = "Python SQL Excel Pandas statistics dashboard data visualization"
    found = ["Python", "SQL", "Excel", "Pandas", "Statistics", "Data Visualization"]
    ranked = rank_job_roles(resume, found, roles)
    assert len(ranked) == 5
    assert ranked.iloc[0]["job_role"] == "Data Analyst"
    gaps = analyze_target_role(found, roles, "Data Analyst")
    assert "Power BI" in gaps["missing"]
