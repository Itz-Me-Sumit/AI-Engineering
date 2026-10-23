import re
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"


FALLBACK = """NovaFlow executes workflows from approved templates. Failed runs enter
a retry queue. Administrators see retry details in the operations dashboard.
NovaSecure records every manual replay. Audit records are retained for 400 days."""


def load_text():
    return FALLBACK

def build_window(text:str , radius:int = 1) -> list[dict]:
    """Build a context window around every sentence.

    Args:
        text: Document text to split into sentences.
        radius: Neighboring sentences included on each side.

    Returns:
        Records containing each focus sentence and window.
    """

    sentences = [
        s.strip()
        for s in re.split( r"(?<=[.!?])\s+", text.replace("\n", " ") )
        if s.strip()
    ]

    records = []

    for idx , sentence in enumerate(sentences , start = 1):
        start , end = max(0 , idx - radius) , min(len(sentence) , idx+radius+1)
        records.append(
            {
                "focus":sentence,
                "window":" ".join(sentences[start : end])
            }
        )

    return records

def keyword_score(query:str , text:str) -> int:
    """Count meaningful words shared by a query and text.

    Args:
        query: Search question to compare.
        text: Candidate text to score.

    Returns:
        Number of matching words.
    """
    terms = set(re.findall(r"[a-z]{3,}", query.lower()))

    return len(terms & set(re.findall(r"[a-z]{3,}", text.lower())))


def main() -> None:
    records = build_window(load_text(), radius=1)
    query = "Where can administrators see failed NovaFlow run details?"
    best = max(records, key=lambda record: keyword_score(query, record["focus"]))
    print(f"[index] {len(records)} sentence records")
    print(f"[query] -> {query}")
    print(f"[focus hit] {best['focus']}")
    print(f"[expanded window] {best['window']}")

if __name__=="__main__":
    main()
     