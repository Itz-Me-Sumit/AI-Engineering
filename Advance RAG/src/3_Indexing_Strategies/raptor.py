from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"
FALLBACK = [
    "NovaFlow automates approvals and operational workflows.",
    "Failed NovaFlow runs can be replayed for fourteen days.",
    "NovaSecure automates access reviews and evidence collection.",
    "NovaSecure security logs are retained for 400 days.",
    "NovaDesk provides a customer support workspace.",
    "Deleted NovaDesk tickets remain recoverable for thirty days.",
]


def load_leaves() -> list[str]:
    """Load the sample leaf passages.

    Returns:
        Passages used to build the RAPTOR tree.
    """
    return FALLBACK

def terms(text: str) -> set[str]:
    """Extract unique searchable terms from text.

    Args:
        text: Text to examine.

    Returns:
        Normalized terms found in the text.
    """
    return set(re.findall(r"[a-z]{4,}", text.lower()))

def summarize(children: list[dict]) -> str:
    """Create a short grounded summary of child tree nodes.

    Args:
        children: Lower-level RAPTOR nodes to summarize.

    Returns:
        A deterministic summary containing important source terms.
    """
    
    # Combine all child text into one source string, removing any existing "Summary:" prefix.
    source = " ".join(child["text"].removeprefix("Summary: ") for child in children)

    # Find TechNova product names mentioned in the source.
    products = sorted(set(re.findall(r"\bNova(?:Flow|Secure|Desk)\b", source)))

    # Common words that should not be included as useful keywords.
    stop = {
        "summary", "topics", "technova", "provides", "with", "from", "that",
        "this", "each", "into", "their", "days", "can", "and", "for", "are",
    }

    # Collect unique keywords that are relevant to the source.
    keywords = []

    # Look for words with at least 4 letters and filter out unhelpful words.
    for word in re.findall(r"[a-z]{4,}", source.lower()):
        if word not in stop and word not in {product.lower() for product in products} and word not in keywords:
            keywords.append(word)

    # Use the detected product names as the summary label, or "TechNova" if none were found.
    label = ", ".join(products) or "TechNova"

    # Keep only the first 7 keywords to create a short summary.
    # The original child nodes still preserve all the detailed information.
    return f"Summary: {label} topics: {', '.join(keywords[:7])}."    

def group_level(nodes: list[dict], level: int) -> list[dict]:
    """Pair nodes and create their summary parents.

    Args:
        nodes: Child nodes to group.
        level: Tree level assigned to new parents.

    Returns:
        Parent nodes containing summaries and child links.
    """

    # Make a copy so the original `nodes` list is not modified.
    # `parents` will store the newly created higher-level nodes.
    remaining, parents = nodes.copy(), []

    # Keep grouping nodes until there are no nodes left.
    while remaining:

        # Take the first node as the starting point for a new group.
        first = remaining.pop(0)

        # Start the group with this node.
        children = [first]

        # If another node is available, find the one most similar to `first`.
        if remaining:
            partner = max(
                remaining,
                key=lambda node: len(terms(first["text"]) & terms(node["text"]))
            )

            # Remove the selected partner so it isn't grouped again.
            remaining.remove(partner)
            children.append(partner)

        # Create a parent node containing the summary and its child nodes.
        parents.append({
            "level": level,
            "text": summarize(children),
            "children": children
        })

    return parents


def build_tree(leaves: list[str]) -> list[list[dict]]:
    """Build summary levels until one root remains.

    Args:
        leaves: Original passages for the lowest level.

    Returns:
        All tree levels from leaves to root.
    """

    # Create level 0 containing the original passages (leaf nodes).
    levels = [[{"level": 0, "text": text, "children": []} for text in leaves]]

    # Keep creating higher levels until only one node (the root) remains.
    while len(levels[-1]) > 1:

        # Group the current level into pairs and create summary parents.
        # `len(levels)` gives the next level number.
        levels.append(group_level(levels[-1], len(levels)))

    return levels


def descend(node: dict, query: str) -> dict:
    """Follow the strongest matches down to a leaf.

    Args:
        node: Summary node where the search begins.
        query: Search question used to choose children.

    Returns:
        Best-matching leaf node.
    """

    # Keep moving down the tree as long as the current node has children.
    while node["children"]:

        # Among the children, choose the one sharing the most words with the query.
        node = max(
            node["children"],
            key=lambda child: len(terms(query) & terms(child["text"]))
        )

    # Once there are no children, we've reached the most relevant leaf.
    return node


def main() -> None:
    """Build a RAPTOR tree and retrieve supporting evidence."""

    # Build the complete RAPTOR tree from the original passages.
    levels = build_tree(load_leaves())

    # Define the question we want to answer.
    query = "How long can failed NovaFlow runs be replayed?"

    # Display how many nodes exist at each level of the tree.
    for level, nodes in enumerate(levels):
        print(f"[tree] level {level}: {len(nodes)} {'leaves' if level == 0 else 'summaries'}")

    # Display the search query.
    print(f"[query] {query}")

    # Find the best-matching node at every tree level.
    # This allows both detailed and high-level searches.
    level_winners = [
        max(nodes, key=lambda node: len(terms(query) & terms(node["text"])))
        for nodes in levels
    ]

    # Display the best match found at each level.
    for winner in level_winners:
        print(f"[level {winner['level']} hit] {winner['text']}")

    # From the summary levels, choose the summary that best matches the query.
    # `[1:]` skips level 0 because it contains the original passages.
    summary_winner = max(
        level_winners[1:],
        key=lambda node: len(terms(query) & terms(node["text"]))
    )

    # Starting from the selected summary, descend through its children
    # until reaching the most relevant original passage.
    evidence = descend(summary_winner, query)

    # Display the original passage that provides the supporting evidence.
    print(f"[descended leaf evidence] {evidence['text']}")


if __name__ == "__main__":
    main()