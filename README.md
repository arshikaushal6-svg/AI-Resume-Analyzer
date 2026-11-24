# AI Resume Analyzer and Job Recommendation System

A beginner-friendly NLP project built with Python and Streamlit. It extracts text from PDF/DOCX resumes, identifies skills, compares the resume with five job roles, recommends the top three roles, identifies skill gaps, and suggests a learning roadmap.

## Features
- PDF and DOCX resume upload
- Text extraction and cleaning
- Skill extraction using a maintainable CSV dictionary
- Five sample job roles
- TF-IDF + cosine similarity matching
- Explainable match score: 70% text similarity + 30% required-skill coverage
- Top three role recommendations
- Missing-skill analysis and a rule-based learning roadmap
- Downloadable text analysis report
- Basic automated tests

## Requirements
- Python 3.10 or newer
- Internet connection for the first-time package installation

## Run on Windows (PowerShell)
1. Extract the ZIP file.
2. Open the extracted `ai_resume_analyzer` folder in VS Code.
3. Open Terminal in VS Code.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again.

6. Install packages:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. Start the application:

   ```powershell
   streamlit run app.py
   ```

8. Streamlit will show a local URL, usually `http://localhost:8501`. Open it in your browser.

## Run tests
From the project folder, with the virtual environment activated:

```powershell
python -m pytest
```

If pytest is not installed, install it with `pip install pytest`.

## Project structure
```text
ai_resume_analyzer/
├── app.py
├── resume_parser.py
├── text_cleaner.py
├── skill_extractor.py
├── job_matcher.py
├── roadmap_generator.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── job_roles.csv
│   └── skill_dictionary.csv
├── tests/
│   └── test_core.py
└── reports/
```

## How the match score works
1. TF-IDF converts the resume and each role description into numerical vectors.
2. Cosine similarity measures how similar the resume text is to each role description.
3. Skill coverage = matched required skills / total required skills.
4. Final score = (0.70 × cosine similarity + 0.30 × skill coverage) × 100.

The score is a comparison estimate, not a probability of employment or a recruiter decision. Results depend on the resume wording and the included job-role dataset.

## Customize the project
- Add or edit roles in `data/job_roles.csv`. Separate required skills with `|`.
- Add skills and aliases in `data/skill_dictionary.csv`. Separate aliases with `|`.
- Add learning suggestions in `roadmap_generator.py`.

## Limitations and responsible use
- Scanned/image-only PDFs may not contain extractable text; OCR is not included in this beginner version.
- Keyword-based skill extraction can miss synonyms or skills described in unusual ways.
- The included role dataset is a small educational example, not a live job-market database.
- A missing keyword does not prove that a candidate lacks a skill.
- The system must be used for guidance, not automatic hiring or rejection. It does not score protected personal attributes.
- Uploaded resumes are processed in memory by this app and are not written to a permanent storage folder. Avoid uploading sensitive documents to public deployments unless you understand the hosting provider's privacy practices.

## Suggested viva explanation
"This project uses NLP techniques to analyze resume text. First, it extracts text from PDF or DOCX files. Then it cleans the text and identifies skills using a predefined skill dictionary. TF-IDF and cosine similarity compare the resume with job-role descriptions. The system combines text similarity and skill coverage to rank roles. Finally, it displays missing skills and a rule-based learning roadmap through a Streamlit dashboard."
