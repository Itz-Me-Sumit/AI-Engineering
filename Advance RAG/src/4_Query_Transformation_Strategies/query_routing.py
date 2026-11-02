from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DATA_DIR = ROOT / "data" / "input"
CORPORA = {
    "security": ["NovaSecure security logs are retained for 400 days.", "Reviewers cannot approve access reviews."],
    "operations": ["Failed NovaFlow runs can be replayed for fourteen days.", "NovaFlow automates workflows."],
    "billing": ["TechNova invoices workspaces monthly.", "Enterprise plans include priority support."],
}


def route(query: str) -> tuple[str, float]:
    """Choose the most relevant corpus for a query.
    
    Args:
        query: The user question or search text.
    Returns: The selected route name and its matched-term coverage.
    """
    # Define keywords that indicate which corpus is most relevant to the query
    # Example: "replay" points toward operations while "invoice" point towards billing.
    signals = {
        "security": {"role", "permission", "audit", "access"},
        "operations": {"novaflow", "workflow", "failed", "replay"},
        "billing": {"price", "invoice", "plan", "cost"}
    }

    # Convert the query into lowercase words containing at least 3 letters.
    # Example: "How long can a failed NovaFlow workflow be replayed?" → {"how", "long", "can", "failed", "novaflow", "workflow", "be", "replayed"}
    words = set(re.findall(r"[a-z]{3,}", query.lower()))

    # Count how many routing keywords from each category appear in the query.
    # Example: operations may score 2 because "novaflow" and "workflow" are present.
    scores = {name: len(words & terms) for name, terms in signals.items()}

    # Select the route with the highest number of matching keywords.
    # Example: {"security": 0, "operations": 2, "billing": 0} → "operations".
    selected = max(scores, key = scores.get)

    # Return the selected route and its matched-term coverage.
    # If no keywords match, return "unknown" with a coverage score of 0.0.
    return (selected, scores[selected]) if scores[selected] else ("unknown", 0.0)

    

def retrieve(query: str, corpus: list[str]) -> str:
    """Find the passage with the greatest term overlap.
    
    Args:
        query: The user question or search text.
        corpus: The passages available for retrieval.
    Returns: The best matching passage, with its index when applicable.
    """    

    words = lambda text: set(re.findall(r"[a-z]{3,}", text.lower()))

    # Compare the query with every passage and return the one with the most shared terms.
    # Example: if passage scores are [2, 4, 1], the second passage is returned.    
    return max(corpus, key = lambda text: len(words(query) & words(text)))


def main() -> None:
    """Run the tutorial demonstration."""
    query = "How long can a failed NovaFlow workflow be replayed?"
    selected, confidence = route(query)

    print(f"[Query] -> {query}")
    print(f"[route] -> {selected} (matched-term coverage={confidence:.2f}), not calibrated confidence")

    if selected == "unknown":
        print("[Fallback] Ask a clarifying question or search all authorized sources.")
        return
    
    print(f"[retrive] -> {retrieve(query, CORPORA[selected])}")
    print(f"[data hint] Real source files can be placed under {DATA_DIR}")

if __name__=="__main__":
    main()