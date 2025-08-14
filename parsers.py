from typing import Optional
import fitz  # PyMuPDF
from docx import Document


def load_pdf(path: str) -> str:
    """Extract text from a PDF file using PyMuPDF."""
    texts = []
    with fitz.open(path) as doc:
        for page in doc:
            texts.append(page.get_text("text"))
    return "\n".join(t for t in texts if t and t.strip())


def load_docx(path: str) -> str:
    """Extract text from a DOCX file."""
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text and p.text.strip())


def load_txt(path: str, encoding: Optional[str] = "utf-8") -> str:
    """Load text from a TXT file."""
    with open(path, "r", encoding=encoding, errors="ignore") as f:
        return f.read()


def load_any(path: str) -> str:
    """Load and extract text from PDF, DOCX, or TXT."""
    lower = path.lower()
    if lower.endswith(".pdf"):
        return load_pdf(path)
    if lower.endswith(".docx"):
        return load_docx(path)
    if lower.endswith(".txt"):
        return load_txt(path)
    raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")
