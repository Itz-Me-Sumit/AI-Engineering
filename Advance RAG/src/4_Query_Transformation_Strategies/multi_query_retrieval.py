import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

DOC_DIR = ROOT / "data" / "input" / "documents"

FALLBACK = [
    "Failed NovaFlow workflow runs can be replayed for fourteen days.",
    "NovaFlow unsuccessful executions remain eligible for rerun for two weeks.",
    "NovaSecure records access-review evidence for administrators.",
]


def load_documents() -> list[str]:
    """Return the documents used by this example.
    
    Returns:
        The sample document passages.
    """    
    return FALLBACK


def generate_queries(query: str) -> list[str]:
    return [
        query,
        "How long is an unsuccessfuly NovaFlow execution eligible for rerun?",
        "What is the NovaFlow workflow replay period after failure?",
    ]


def score(query: str, text: str) -> int:
    """Measure keyword overlap between a query and passage.
    
    Args:
        query: The user question or search text.
        text: The text to inspect or compare.
    Returns: The number of meaningful terms shared by both texts.
    """
    
    # Create a small function that converts text into lowercase words of at least 4 characters.
    words = lambda value: set(re.findall(f"[a-z]{4,}", value.lower()))

    return len(words(query) & words(text))

def main() -> None:
    """Run the tutorial demonstration"""
    query = "How long is a failed Novaflow run replayable?"
    documents, merged = load_documents(), {}

    for variation in generate_queries(query):
        ranked = sorted(enumerate(documents), key = lambda pair: score(variation, pair[1]), reverse=True)
        doc_id, text = ranked[0]
        merged[doc_id] = text

        print(f"[query] {variation}\n -> document {doc_id}: {text[:100]}")

    print(f"[merge] {len(merged)} unique documents from 3 query perspectives.")

if __name__=="__main__":
    main()