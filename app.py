import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from parsers import load_any
from analyzer import analyze_case_text

# ---------- Env ----------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------- Streamlit Page ----------
st.set_page_config(page_title="Case Study Analyzer (Gemini)", layout="wide")
st.title("🧭 Agentic AI — Case Study Analyzer (Gemini)")

if not API_KEY:
    st.error(
        "GOOGLE_API_KEY not found. Create a `.env` file in your project root:\n\n"
        "GOOGLE_API_KEY=YOUR_GOOGLE_GEMINI_API_KEY_HERE"
    )
    st.stop()

# ---------- Sidebar / Controls ----------
with st.sidebar:
    st.header("⚙️ Settings")
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.2, 0.05)
    max_chars = st.number_input(
        "Max characters per chunk (advanced)", min_value=1000, max_value=30000, value=6000, step=500
    )
    overlap = st.number_input(
        "Chunk overlap (advanced)", min_value=0, max_value=5000, value=600, step=50
    )
    st.caption(
        "Tip: Larger chunks can capture more context but may be slower. Overlap helps maintain continuity."
    )

uploaded = st.file_uploader("Upload case study file (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])

col_a, col_b = st.columns([1, 1])
with col_a:
    run_btn = st.button("🔎 Analyze", type="primary")
with col_b:
    clear_btn = st.button("🧹 Clear")

if clear_btn:
    st.experimental_rerun()

# ---------- Run ----------
if run_btn:
    if not uploaded:
        st.warning("Please upload a PDF/DOCX/TXT file first.")
        st.stop()

    # Save to a temp file (preserve extension)
    suffix = "." + uploaded.name.split(".")[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    # Extract text
    with st.spinner("📄 Extracting text..."):
        try:
            raw_text = load_any(tmp_path)
        except Exception as e:
            st.error(f"Failed to extract text: {e}")
            st.stop()

    if not raw_text or not raw_text.strip():
        st.error("No readable text found in the uploaded file.")
        st.stop()

    st.success("Text extracted. Running analysis…")

    # Analyze
    with st.spinner("🧠 Analyzing with Gemini…"):
        try:
            report_md = analyze_case_text(
                raw_text,
                temperature=temperature,
                max_chars=max_chars,
                overlap=overlap,
            )
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            st.stop()

    st.success("✅ Done! Your report is ready.")
    st.download_button(
        "⬇️ Download Markdown Report",
        report_md,
        file_name="case_report.md",
        mime="text/markdown",
    )
    st.markdown(report_md)
