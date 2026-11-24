import re

def clean_text(text):
    """Normalize text while preserving useful technical terms such as C++, C#, and .NET."""
    text = text.lower()
    text = text.replace("c sharp", "c#").replace("dot net", ".net")
    text = re.sub(r"[\r\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    # Keep letters, digits, common technical punctuation, and spaces.
    text = re.sub(r"[^a-z0-9+#./_\- ]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
