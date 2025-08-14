import os
from dotenv import load_dotenv
from typing import List
import google.generativeai as genai

from utils import clean_text, chunk_text, merge_distilled_json

load_dotenv()
_API_KEY = os.getenv("GOOGLE_API_KEY")
if not _API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set. Create a .env file with your key.")

genai.configure(api_key=_API_KEY)
'''
# Configure Gemini using GOOGLE_API_KEY
_API_KEY = os.getenv("GOOGLE_API_KEY")
if not _API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not set. Create a .env file with your key.")

genai.configure(api_key=_API_KEY)
'''
# Choose a sensible, generally-available text model
# You can switch to "gemini-1.5-pro" if your quota supports it
_MODEL_NAME = "gemini-1.5-flash"


def _prompt_for_chunk(case_text: str) -> str:
    """Builds the instruction prompt for each chunk. Keep it short; we add the chunk separately."""
    return (
        "You are an expert business analyst. Read the following case-study excerpt and produce a **concise, structured**"
        " markdown summary with:\n"
        "1) Executive Summary\n"
        "2) Key Facts & Figures\n"
        "3) Problems / Pain Points\n"
        "4) Root-Cause Analysis\n"
        "5) Opportunities / Recommendations\n"
        "6) Risks & Assumptions\n"
        "Use bullet points where helpful. Keep it crisp and factual. Do not invent data.\n\n"
        "Excerpt:\n"
        f"{case_text}"
    )


def _distill_prompt(parts_markdown: List[str]) -> str:
    """Combines multiple per-chunk summaries into a single, unified report."""
    joined = "\n\n---\n\n".join(parts_markdown)
    return (
        "You are an expert editor. Merge these partial markdown summaries into a single **cohesive final report**."
        " Remove duplicates, resolve conflicts, and keep a consistent tone."
        " Preserve the headings in this order:\n"
        "## Executive Summary\n"
        "## Key Facts & Figures\n"
        "## Problems / Pain Points\n"
        "## Root-Cause Analysis\n"
        "## Opportunities / Recommendations\n"
        "## Risks & Assumptions\n\n"
        "Keep it concise and avoid repetition. Here are the parts to merge:\n\n"
        f"{joined}"
    )


def _run_gemini(prompt: str, temperature: float) -> str:
    model = genai.GenerativeModel(_MODEL_NAME)
    resp = model.generate_content(
        prompt,
        generation_config={"temperature": float(temperature)},
    )
    # Handle safety/blocked/empty responses robustly
    if not hasattr(resp, "text") or not resp.text:
        # Sometimes content is returned as parts
        try:
            return "".join(p.text for p in resp.candidates[0].content.parts if getattr(p, "text", None))
        except Exception:
            return ""
    return resp.text


def analyze_case_text(
    case_text: str,
    temperature: float = 0.2,
    max_chars: int = 6000,
    overlap: int = 600,
) -> str:
    """
    Analyze a large case-study text by chunking it, summarizing each piece,
    and fusing the parts into a unified markdown report.
    """
    cleaned = clean_text(case_text)
    chunks = chunk_text(cleaned, max_chars=max_chars, overlap=overlap)

    partial_markdowns: List[str] = []
    for i, ch in enumerate(chunks, start=1):
        prompt = _prompt_for_chunk(ch)
        md = _run_gemini(prompt, temperature=temperature)
        if not md:
            md = f"_No output generated for chunk {i}_"
        partial_markdowns.append(md)

    # Final distillation across all parts
    final_prompt = _distill_prompt(partial_markdowns)
    final_md = _run_gemini(final_prompt, temperature=max(0.1, temperature - 0.1))

    # Fallback if distillation returns empty
    if not final_md.strip():
        final_md = "\n\n---\n\n".join(partial_markdowns)

    # Ensure nice H2 headings for GitHub/Streamlit rendering
    if not final_md.lstrip().startswith("#"):
        final_md = "# Case Study Analysis\n\n" + final_md

    return final_md
