import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_job_roles(path):
    return pd.read_csv(path).fillna("")

def _required_skills(row):
    return [x.strip() for x in str(row["required_skills"]).split("|") if x.strip()]

def rank_job_roles(resume_text, found_skills, roles_df):
    """Rank roles using 70% TF-IDF similarity and 30% required-skill coverage."""
    documents = [resume_text] + [
        f"{row['job_role']} {row['description']} {row['required_skills'].replace('|', ' ')}"
        for _, row in roles_df.iterrows()
    ]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(documents)
    similarities = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    found = {s.lower() for s in found_skills}
    results = []
    for index, (_, row) in enumerate(roles_df.iterrows()):
        required = _required_skills(row)
        matched = [s for s in required if s.lower() in found]
        coverage = len(matched) / len(required) if required else 0
        score = (0.70 * float(similarities[index]) + 0.30 * coverage) * 100
        results.append({
            "job_role": row["job_role"],
            "match_score": round(min(score, 100), 1),
            "matched_count": len(matched),
            "required_count": len(required)
        })
    return pd.DataFrame(results).sort_values("match_score", ascending=False).reset_index(drop=True)

def analyze_target_role(found_skills, roles_df, selected_role):
    row = roles_df.loc[roles_df["job_role"] == selected_role].iloc[0]
    required = _required_skills(row)
    found = {s.lower() for s in found_skills}
    matched = [s for s in required if s.lower() in found]
    missing = [s for s in required if s.lower() not in found]
    return {"matched": matched, "missing": missing}
