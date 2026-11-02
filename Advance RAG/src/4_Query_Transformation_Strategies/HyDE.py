from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"
FALLBACK = [
    "Failed NovaFlow runs can be replayed for fourteen days after failure.",
    "NovaDesk exports remain available for seven days.",
    "NovaSecure security logs are retained for 400 days.",
]

def load_documents() -> list[str]:
    return FALLBACK

def hypothetical_answer(query: str) -> str:
    """Create a hypothetical answer to guide document retrieval.
    
    Args:
        query: The user question or search text.
    Returns: A generated passage used only as a search probe.
    """    

    # Check whether the query is about NovaFlow and mentions either replay or failure
    # Example: "How can a failed NovaFlow run be replayed?" -> condition is True
    if "novaflow" in query.lower() and any(word in query.lower() for word in ("replay", "failed")):

        return (
            "A failed NovaFlow worflow run remains eligible for a replay "
            "defined retention period after the original exucution fails."
        )
    
    return "TechNova documentation states a specific product policy and retention period."


def score(query: str, text: str) -> int:
    """Measure keyword overlap between a query and passage.
    
    Args:
        query: The user question or search text.
        text: The text to inspect or compare.
    Returns: The number of meaningful terms shared by both texts.
    """
    terms = lambda value: set(re.findall(r"[a-z]{4,}", value.lower()))  
    return len(terms(query) & terms(text))


def main() -> None:
    """Run the tutorial script for hyde implementation"""
    query = "How long can a failed NovaFlow run be replayed?"
    hyde_text = hypothetical_answer(query)
    docs = load_documents()
    direct = max(docs, key = lambda text: score(query, text))
    expanded = max(docs, key = lambda text: score(hyde_text, text))


    print(f"[query] -> {query}")
    print(f"[hypothetical-not evidence] {hyde_text}")
    print(f"[direct hit] {direct[:120]}")
    print(f"[HyDE hit] {expanded[:120]}")
    print("[grounding] Only the retrieved source is evidence; the hypothetical passage is a search probe")

if __name__=="__main__":
    main()