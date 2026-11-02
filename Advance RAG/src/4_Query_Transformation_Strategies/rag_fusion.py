"""
Query 1:
1. Document A
2. Document B

Query 2:
1. Document B
2. Document A

Query 3:
1. Document B
2. Document C

Position 1 → 1 / 61 = 0.01639
Position 2 → 1 / 62 = 0.01613
Position 3 → 1 / 63 = 0.01587

"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

DOC_DIR = ROOT / "data" / "input" / "documents"

FALLBACK = [
    "Failed NovaFlow runs can be replayed for fourteen days.",
    "NovaFlow unsuccessful executions remain replayable for two weeks.",
    "NovaSecure security logs are retained for 400 days.",
    "NovaDesk deleted tickets are recoverable for thirty days.",
]


def documents() -> list[str]:
    """Return the documents used by this example.
    
    Returns:
        The sample document passages.
    """
    return FALLBACK


def terms(text: str) -> set[str]:
    """Extract normalized search terms from text.
    
    Args:
        text: The text to inspect or compare.
    Returns: A set of normalized terms.
    """
    return set(re.findall(r"[a-z]{4,}", text.lower()))


def rank(query: str, docs: list[str]) -> list[int]:
    """Rank matching documents by keyword overlap.
    
    Args:
        query: The user question or search text.
        docs: The documents to score.
    Returns: Matching document indexes in descending relevance order.
    """
    # Calculate the keyword-overlap score for every document and store (score, document index).
    # Example: docs = ["NovaFlow replay", "NovaSecure logs"] → [(1, 0), (0, 1)].
    scored = [(len(terms(query) & terms(text)), index) for index, text in enumerate(docs)]

    # Remove documents with zero overlap and return the remaining indexes in descending score order.
    # Example: [(2, 1), (1, 0), (0, 2)] → [1, 0].
    # Zero-score documents contribute no evidence and must not gain RRF points.
    return [index for score, index in sorted(scored, reverse=True) if score > 0]


def main() -> None:
    """Run the tutorial demonstration."""

    # Define three different query perspectives for the same information need.
    # Each query uses slightly different wording to improve retrieval coverage.
    queries = [
        "How long can a failed NovaFlow run be replayed?",
        "NovaFlow unsuccessful execution rerun period",
        "NovaFlow workflow replay eligibility",
    ]

    # Load the documents, create an empty dictionary for fused scores, and set RRF's k value.
    # k=60 is the standard constant used here to reduce the impact of ranking position.
    docs, fused, k = documents(), {}, 60

    # Process each query independently and retrieve its ranked list of documents.
    for query in queries:
        ranking = rank(query, docs)

        # Display the top 3 document indexes returned for this query.
        # Example: [0, 1] means document 0 ranked first and document 1 second.
        print(f"[ranking] {query} -> {ranking[:3]}")

        # Go through each document and its position in the ranking.
        for position, doc_id in enumerate(ranking, 1):
            # Add an RRF score based on the document's position in this ranking.
            # Earlier positions receive a higher score: 1/(60+1), 1/(60+2), etc.
            fused[doc_id] = fused.get(doc_id, 0.0) + 1 / (k + position)

    # Sort documents by their accumulated RRF score, from highest to lowest.
    # Documents ranked well across multiple queries naturally move toward the top.
    final = sorted(fused, key=fused.get, reverse=True)

    # Print a heading before showing the final fused ranking.
    print("[fusion] final order")

    # Display the top 3 documents after combining all query rankings.
    for doc_id in final[:3]:
        # Print the final RRF score and the first 100 characters of the document.
        # Example: score=0.0489 doc=NovaFlow unsuccessful executions remain replayable...
        print(f"  score={fused[doc_id]:.4f} doc={docs[doc_id][:100]}")


if __name__ == "__main__":
    main()