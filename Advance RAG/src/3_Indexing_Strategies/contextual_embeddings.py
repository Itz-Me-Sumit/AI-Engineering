from collections import Counter
from math import log , sqrt
from pathlib import Path
import sys
import re

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0 , str(ROOT))

DOC_DIR = ROOT / "data" / "input" / "documents"

FALLBACK = """# NovaFlow Guide
## Synchronization
It runs every fifteen minutes and retries failed documents.
## NovaSecure Security
It stores audit events for one year."""


def load_text():
    return FALLBACK , "NovaFlow Guide"

def tfidf_vectors( texts:list[str] ) -> list[dict[str,float]]:
    """Create a TF-IDF vector for each input text.

    Args:
        texts: Text passages to convert into vectors.

    Returns:
        Sparse term-to-weight vectors in input order.
    """

    tokenized = [re.findall(r"[a-z]{3,}" , text.lower()) for text in texts]

    document_frequency = Counter(
        term 
        for terms in tokenized 
        for term in set(terms)
    )

    total_word_count = len(texts)
    vectors = []

    for terms in tokenized:
        freq = Counter(terms)
        vectors.append(
            {
                term : value * (
                    log(
                        (1+total_word_count) / (1 + document_frequency[term])
                    )
                ) + 1
                for term , value in freq.items()
            }
        )

    return vectors


def similarity(left:dict[str,float] , right:dict[str,float]) -> float:
    """Measure similarity between two TF-IDF vectors.

    Args:
        left: First term-weight vector.
        right: Second term-weight vector.

    Returns:
        Cosine similarity from zero to one.
    """
    dot_prod = sum(value*right.get(term , 0.0) for term , value in left.items())
    left_norm = sqrt(
        sum(
            value*value 
            for value in left.values()
        )
    )
    right_norm = sqrt(
        sum(
            value*value 
            for value in right.values()
        )
    )

    return dot_prod / (
        left_norm * right_norm
    ) if left_norm and right_norm else 0.0

def main():
    text , title = load_text()
    section , records = "Overview" , []

    for line in text.splitlines():
        if line.startswith("#"):
            section = line.lstrip("#").strip()
        elif line.strip():
            context = f"TechNova Document {title}; section {section}"
            records.append(
                {
                    "raw": line,
                    "contextual": context+line
                }
            )

    query = "What is the NovaFlow synchronization schedule?"

    raw_texts = [record["raw"] for record in records]
    contextual_texts = [record["contextual"] for record in records]

    vectors = tfidf_vectors([query , *raw_texts , *contextual_texts])

    query_vector = vectors[0]
    raw_vectors = vectors[1: 1+len(records)]
    contextual_vectors = vectors[1+len(records):]

    raw_index = max(
        range(len(records)),
        key = lambda i : similarity(query_vector , raw_vectors[i])
    )

    context_index = max(
        range(len(records)),
        key = lambda i : similarity(query_vector , contextual_vectors[i])
    )

    print(f"[index] embedded {len(records)} passages two ways.")
    print(f"[raw score = {similarity(query_vector , raw_vectors[raw_index]):.3f}] {records[raw_index]['raw']}")
    print(f"[context score = {similarity(query_vector , contextual_vectors[context_index]):.3f}] {records[context_index]['contextual']}")


if __name__ == "__main__":
    main()
