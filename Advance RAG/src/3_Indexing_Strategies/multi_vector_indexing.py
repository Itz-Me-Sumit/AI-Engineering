from pathlib import Path
import uuid
import sys
import re 


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"

FALLBACK = [
    ("NovaFlow Operations", "Failed NovaFlow runs can be replayed for fourteen days. The dashboard shows retry details."),
    ("NovaSecure Security", "NovaSecure automates access reviews. Security logs are retained for 400 days."),
    ("NovaDesk Support", "NovaDesk exports are retained for seven days. Deleted tickets remain recoverable for thirty days."),
]

def load_documents() -> list[tuple[str, str]]:
    return FALLBACK

def terms(text: str) -> set[str]:
    """Extract unique searchable terms from text.

    Args:
        text: Text to examine.

    Returns:
        Normalized terms found in the text.
    """    
    return set(re.findall(r"[a-z]{4,}", text.lower()))

def build_index(documents: list[tuple[str, str]]) -> tuple[dict, list[dict]]:
    """Create several search representations per document.

    Args:
        documents: Document titles paired with body text.

    Returns:
        Source storage and searchable vector records.
    """

    # `store` keeps the original documents, while `vectors` stores
    # different searchable representations of each document.
    store, vectors = {}, []

    for title, body in documents:

        doc_id = uuid.uuid5(uuid.NAMESPACE_URL, title).hex[:8]
        store[doc_id] = body

        sentences = re.split(r"(?<=[.!?])\s+", body)
        summary = sentences[0]

        # Count how often each meaningful term appears in the document.        
        counts = {
            term: body.lower().count(term) 
            for term in terms(body)
        }

        # Select the 8 most frequent terms to create a keyword representation.
        # `-counts[term]` sorts by frequency from highest to lowest.        
        keywords = " ".join(sorted(counts, key = lambda term: (-counts[term], terms))[:8])

        # Create a question that represents what a user might ask about this document.   
        question = f"What does the {title} guide say about the retention and operations?"     

        # Create multiple search representations of the same document.
        # Each representation can match a query in a different way.        
        for kind, text in [
            ("title", title),
            ("summary", summary),
            ("keywords", keywords),
            ("question", question),
            ("body", body)
        ]:
            vectors.append({
                "doc_id": doc_id,
                "kind": kind,
                "text": text,
                "tokens": terms(text)
            })

    return store, vectors


def rank_documents(query: str, vectors: list[dict]) -> list[dict]:
    """Rank document representations and remove duplicate source documents.

    Args:
        query: Search question used for ranking.

        vectors: Indexed representations linked to source documents.

    Returns:
        Best matching representation for each ranked document.
    """
    # Convert the query into a set of searchable terms.  
    query_terms = terms(query)

    # Rank all representations by the number of query terms they contain.
    # More matching terms = higher ranking.
    representation_ranking = sorted(
        vectors,
        key = lambda item: (len(query_terms & item["tokens"])),
        reverse=True
    )

    # This dictionary will keep only one result for each doc
    grouped: dict[str, dict] = {}

    for representation in representation_ranking:
        doc_id = representation["doc_id"]

        # Keep the first representation we encounter for each document.
        # Since results are already ranked, this is the document's best match.
        if doc_id not in grouped:
            grouped[doc_id] = {
                "doc_id": doc_id,
                "score": len(query_terms & representation["tokens"]),
                "matched_kind": representation["kind"],
                "matched_text": representation["text"],
            }

    return list(grouped.values())


def main() -> None:
    """Build the index and demonstrate deduplicated retrieval."""

    # Build the searchable index from the loaded documents.
    # `store` contains original documents; `vectors` contains their search representations.
    store, vectors = build_index(load_documents())

    # Define the question we want to search for.
    query = "How long are NovaSecure security logs retained?"

    # Rank the representations and remove duplicate source documents.
    ranked_documents = rank_documents(query, vectors)

    # Take the highest-ranked document as the best match.
    winner = ranked_documents[0]

    # Show how many searchable representations were created for the source documents.
    print(f"[index] {len(vectors)} vectors represent {len(store)} source documents")

    # Display the search question.
    print(f"[query] {query}")

    # Show how many representation matches were reduced to unique documents.
    print(f"[deduplicate] {len(vectors)} representation hits -> "
          f"{len(ranked_documents)} unique documents")

    # Show which representation produced the best match and its score.
    # `[:100]` limits the displayed text to the first 100 characters.
    print(f"[match] representation={winner['matched_kind']} "
          f"score={winner['score']} text={winner['matched_text'][:100]}")

    # Use the winning document ID to retrieve and display the original source text.
    # `[:180]` displays only the first 180 characters.
    print(f"[source] {store[winner['doc_id']][:180]}")


if __name__ == "__main__":
    main()