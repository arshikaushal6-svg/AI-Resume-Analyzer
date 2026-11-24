from io import BytesIO
from pypdf import PdfReader
from docx import Document

def extract_resume_text(uploaded_file, filename):
    """Extract text from an uploaded PDF or DOCX file without saving it permanently."""
    content = uploaded_file.getvalue()
    lower_name = filename.lower()
    if lower_name.endswith(".pdf"):
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if lower_name.endswith(".docx"):
        document = Document(BytesIO(content))
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
        # Also read text inside tables, which are common in resumes.
        for table in document.tables:
            for row in table.rows:
                paragraphs.extend(cell.text for cell in row.cells if cell.text.strip())
        return "\n".join(paragraphs)
    raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
