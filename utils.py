import re
from typing import List

# Sensible defaults; can be overridden from app.py controls
MAX_CHARS = 6000
OVERLAP = 600


def clean_text(text: str) -> str:
    """Light cleanup: collapse whitespace while preserving paragraph breaks."""
    # Normalize Windows/Mac newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse multiple spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)
    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, max_chars: int = MAX_CHARS, overlap: int = OVERLAP) -> List[str]:
    """
    Chunk by characters (fast + safe for LLM context windows).
    Overlap preserves continuity between chunks.
    """
    text = text.strip()
    n = len(text)
    if n <= max_chars:
        return [text] if text else []

    chunks: List[str] = []
    start = 0
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == n:
            break
        start = max(0, end - overlap)
    return chunks


def merge_distilled_json(parts: list) -> dict:
    """
    Utility kept in case you later want to aggregate structured JSON outputs.
    Not used in the current markdown-only flow, but harmless to keep.
    """
    from collections import defaultdict

    merged = defaultdict(list)
    for p in parts:
        for k, v in p.items():
            if isinstance(v, list):
                merged[k].extend(v)
            else:
                merged[k].append(v)
    return {k: "\n".join(str(x) for x in v if x) for k, v in merged.items()}
