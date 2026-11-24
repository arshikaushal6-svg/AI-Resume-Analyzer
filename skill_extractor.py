import re
import pandas as pd

def load_skill_dictionary(path):
    return pd.read_csv(path).fillna("")

def _contains_phrase(text, phrase):
    phrase = str(phrase).strip().lower()
    if not phrase:
        return False
    # Phrase boundaries prevent matching e.g. "R" inside unrelated words.
    pattern = r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])"
    return re.search(pattern, text.lower()) is not None

def extract_skills(cleaned_text, skill_df):
    found = []
    for _, row in skill_df.iterrows():
        skill = str(row["skill"]).strip()
        aliases = [x.strip() for x in str(row["keywords"]).split("|") if x.strip()]
        if any(_contains_phrase(cleaned_text, alias) for alias in [skill] + aliases):
            found.append(skill)
    return sorted(set(found), key=str.lower)
