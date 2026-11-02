from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"
FALLBACK = [
    "TechNova access governance follows least privilege and auditable role assignment.",
    "NovaSecure owners may approve access reviews; reviewers can inspect evidence.",
    "NovaSecure administrators review role assignments every quarter.",
]

def documents() -> list[str]:
    return FALLBACK


def step_back(query: str) -> str:
    """Turn a specific query into a broader background question.
    
    Args:
        query: The user question or search text.
    Returns: A broader question related to the original query.
    """    

    if any(word in query.lower() for word in ("reviewer", "owner", "access", "permission", "role")):
        return "What access governance principes control TechNova workspace permission?"
    
    return "What broader TechNova concept governs this behaviour?"

def retrieve(query: str, docs: list[str]) -> str:
    """Find the passage with the greatest term overlap.
    
    Args:
        query: The user question or search text.
        docs: The documents to score.
    Returns: The best matching passage, with its index when applicable.
    """    
    terms = lambda value: set(re.findall(r"[a-z]{4,}", value.lower()))
    return max(docs, key = lambda text: len(terms(query) & terms(text)))

def main() -> None:
    """Run the tut demonstration for step back prompting"""
    query = "Can a NovaSecure reviewer approve an access review?"
    broad = step_back(query)
    docs = documents()

    print(f"[specific] -> {query}")
    print(f"[step back] -> {broad}")
    print(f"[background] {retrieve(broad, docs)[:140]}")
    print(f"[specific evidence] {retrieve(query, docs)[:140]}")

if __name__=="__main__":
    main()