from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"
DOCUMENTS = [
    "Failed NovaFlow workflow runs can be replayed for fourteen days.",
    "NovaSecure access reviews support reviewer and owner roles.",
    "NovaDesk deleted tickets remain recoverable for thirty days.",
    "TechNova workspace invoices are issued monthly.",
]

def load_documents() -> list[str]:
    """Return the documents used by this example.
    
    Returns:
        The sample document passages.
    """
    return DOCUMENTS

def rewrite(query:str) -> str:
    """Convert a conversational question into a focused search query.
    
    Args:
        query: The user question or search text.
    Returns: A normalized standalone search query.
    """

    # Example: "Could you tell me..." → "how long a failed flow can be replayed?"
    query = re.sub(r"^(?:(?:could you|please|tell me|do you know)\s+)+", "", query, flags=re.I)
    aliases = {
        "flow" : "NovaFlow Workflow",
        "permission" : "NovaSecure access control",
        "bill" : "workspace",
    }

    for short , canonical in aliases.items():
        query = re.sub(rf"\b{short}\b", canonical, query, flags=re.I)

    return re.sub(r"[?!]+", "", query).strip()


def terms(text: str) -> set[str]:
    """Extract normalized search terms from text.
    
    Args:
        text: The text to inspect or compare.
    Returns: A set of normalized terms.
    """    
    return set(re.findall(r"[a-z]{4,}", text.lower()))



def main() -> None:
    original = "Could you tell me how long a failed flow can be replayed?"
    rewritten = rewrite(original)
    documents = load_documents()
    best = max(documents, key = lambda text: len(terms(rewritten) & terms(text)))

    print(f"[original] -> {original}")
    print(f"[rewritten] -> {rewritten}")
    print(f"[retrieve] -> {best}")


if __name__ == "__main__":
    main()