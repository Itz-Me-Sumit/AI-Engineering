import re
import sys
import uuid
from pathlib import Path



ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"


FALLBACK = """NovaFlow is TechNova's workflow automation engine. It runs approvals and
operational tasks. Failed workflow runs can be replayed for fourteen days.

NovaSecure protects each NovaFlow workspace. Administrators assign reviewer or
owner roles. Every permission change creates an immutable audit event."""


def load_text()->str:
    """Load the sample document text.

    Returns:
        Text used by the chunking example.
    """
    return FALLBACK

def build_hierarchy(text:str) -> tuple[ dict[str , str] , list[dict] ]:
    
    """Create paragraph parents and sentence children.

    Args:
        text: Document text to organize.

    Returns:
        Parent paragraphs and their linked child records.
    """ 

    # Ex : "  paragraph1\n\nparagraph2 ->> ["paragraph1" , "paragraph2"]  "
    paragraphs = [ 
        p.replace( "\n" , " " ).strip() 
        for p in re.split(r"\n\s*\n", text) 
        if p.strip() 
    ]

    parents , children = {} , []

    for paragraph in paragraphs:

        # Example -> "RAG Helps Retrieve Relevent Info"
        # Might get and id such as this one "a8098c1a"
        parent_id = uuid.uuid5(uuid.NAMESPACE_URL , paragraph).hex[:8]
        parents[parent_id] = paragraph

        # Example: "RAG is useful. It retrieves context."
        # becomes: ["RAG is useful.", "It retrieves context."]
        for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
            if sentence:
                children.append(
                    {
                        "parent_id" : parent_id,
                        "text" : sentence
                    }
                )
    return parents , children

def overlap_score(query:str , text:str) -> int:
    """Count search terms shared by a query and text.

    Args:
        query: Search question to compare.
        text: Candidate text to score.

    Returns:
        Number of shared terms.
    """

    # Example : "How does RAG Improve Retrieval"
    # Terms : {"How" , "does" , "RAG" , ... , } -> breaking down into unique terms

    # this will extract words of atleast 3 letters from query
    terms = set(
        re.findall(
            r"[a-z]{3,}",
            query.lower()
        )
    )

    # Counts How many commnon words there are.
    return len(
        terms &
        set(
            re.findall(
                r"[a-z]{3,}",
                text.lower()
            )
        )    
    )

def main():
    text = load_text()
    parents , children = build_hierarchy(text)
    print(f"[Index] : {len(children)} children, linked to {len(parents)} parents")

    query = """
        which permission change creates ans immutable audit event?
    """

    # Example:
    # Child 1 -> score 3
    # Child 2 -> score 1
    # Child 3 -> score 4

    # After sorting:
    # Child 3 -> score 4 
    # Child 1 -> score 3
    # Child 2 -> score 1

    ranked = sorted(
        children,
        key = lambda child : overlap_score(query , child["text"]),
        reverse = True
    )

    best = ranked[0]
    print(f"[query] -> {query}")
    print(f"[child match] -> {best['text']}")
    print(f"[Expanded parent] -> {parents[best['parent_id']]}")


if __name__ == "__main__":
    main()