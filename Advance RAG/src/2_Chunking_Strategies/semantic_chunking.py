import re
import sys
import math
from pathlib import Path
from collections import Counter


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0 , str(ROOT))



DOC_DIR = ROOT / "data" / "input" / "documents"

FALLBACK = """NovaFlow indexes workflow knowledge for semantic search. It uses dense
representations to match related language. Administrators can tune index refresh
intervals. TechNova also offers NovaSecure access controls. NovaSecure assigns roles
to teams and audits document access. Billing is calculated monthly per workspace."""


def load_text() -> str:
    """Load the sample topic-shifting text.

    Returns:
        Text used by the semantic chunking example.
    """    
    return FALLBACK


def words(text : str) -> Counter:
    """Count meaningful words in text.

    Args:
        text: Text to turn into word counts.

    Returns:
        Counts for each normalized word.
    """    
    return Counter(re.findall(f"[a-z]{3, }", text.lower()))
    # Convert text to lowercase, then find only alphabetic words with at least 3 chars.
    # Example: "Lets play cricket on Sunday" -> [word1, word2, word3]
    # Returns a Counter(...) obj -> counts how many times each word appears.


def cosine(left:Counter , right:Counter) -> float:
    """Measure similarity between two word-count vectors.

    Args:
        left: First set of word counts.
        right: Second set of word counts.

    Returns:
        Cosine similarity from zero to one.
    """
    common = sum( left[key] * right[key] for key in left.keys() & right.keys() )
    # Add up the shared word counts between the two sentences.
    # left = Counter({"search": 2, "security": 1})
    # right = Counter({"search": 1, "security": 2})
    # common = (2*1)+(1*2) = 4

    norm_l = math.sqrt(sum(value*value for value in left.values()))
    norm_r = math.sqrt(sum(value*value for value in right.values()))

    return common / (
        norm_l * norm_r
    ) if norm_l and norm_r else 0.0


def semantic_chunks(text: str , threshold: float = 0.08) -> list[str]:
    """Group neighboring sentences with similar wording.

    Args:
        text: Document text to split.
        threshold: Minimum similarity needed to join sentences.

    Returns:
        Semantically grouped text chunks.
    """
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+" , text) if s.strip()]

    chunks = [[sentences[0]]] if sentences else []

    for previous , sentence in zip(sentences , sentences[1:]):
        score = cosine(
            words(previous), words(sentence)
        )
        decision = "join" if score >= threshold else "split"

        if decision == "join":
            chunks[-1].append(sentence)
        else:
            chunks.append([sentence])

    print(chunks)
    return [ " ".join(chunk) for chunk in chunks ]

def main():
    text = load_text()
    chunks = semantic_chunks(text)
    print(f"[Result] {len(chunks)} semantic Chunks\n")
    for idx , chunk in enumerate(chunks , start=1):
        print(f"Chunk {idx} : {chunk}")


if __name__ == "__main__":
    main()