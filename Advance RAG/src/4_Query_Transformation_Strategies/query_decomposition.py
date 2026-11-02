from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"
FALLBACK = [
    "Failed NovaFlow runs can be replayed for fourteen days.",
    "NovaSecure security logs are retained for 400 days.",
    "NovaDesk exports are retained for seven days.",
]

def load_documents() -> list[str]:
    """Return the documents used by this example.
    
    Returns:
        The sample document passages.
    """    
    return FALLBACK

def decompose(query: str) -> list[str]:
    # Split only at a new interrogative clause; "research and development"
    # should remain one semantic unit.
    """Split a multi-part question into focused subqueries.
    
    Args:
        query: The user question or search text.
    Returns: Focused subqueries that cover the original question.
    """    

    # split the question whenever "and" is followed by a new question word.
    # Example: "...replayed and how long..." -> two separate subqueries.
    parts = re.split(r"\s+and\s+(?=(?:how|what|when|where|which|who)\b)",
             query.strip(" ?"), flags=re.I)
    
    # clean each part, capitalize its first letter and add a question mark.
    # example: "how long can X run" -> "How long can X run?"
    return [part.strip().capitalize() + "?" for part in parts if part.strip()]


def score(query: str, text: str) -> int:
    """Measure keyword overlap between a query and passage.
    
    Args:
        query: The user question or search text.
        text: The text to inspect or compare.
    Returns: The number of meaningful terms shared by both texts.
    """

    # Convert the text into lowercase words containing at least 4 characters/letters.
    words = lambda value: set(re.findall(r"[a-z]{4,}", value.lower()))    


    return len(words(query) & words(text))

def main() -> None:
    """Run the tutorial demonstration for query decomposition."""

    query = "How long can NovaFlow runs be replayed and how long NovaSecure retain security logs?"
    docs = load_documents()
    subqueries = decompose(query)

    print(f"[decompose] <-> {len(subqueries)} subqueries.")

    # create an empty list to collect the best evidence for each subquery.
    evidence = []

    for subquery in subqueries:

        # find the document with the highest keyword-overlap score for this subquery
        # example: "NovaFlow replay" -> "Failed NovaFlow runs can be replayed for fourteen days."
        hit = max(docs, key = lambda text: score(subquery, text))
        evidence.append(hit)

        print(f"    Q: {subquery}\n    E: {hit[:120]}")

    print(f"[combine] collected {len({item for item in evidence})} distinct evidence passages")

if __name__=="__main__":
    main()