from pathlib import Path
import re
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"
FALLBACK = """Failed NovaFlow runs can be replayed for fourteen days.
NovaDesk exports are retained for seven days.
NovaSecure security logs are retained for 400 days."""


def load_passages() -> list[str]:
    """Split the sample text into useful passages.

    Returns:
        Nontrivial passages from the sample.
    """
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", FALLBACK) if len(s.split()) > 3]


def keywords(text: str) -> set[str]:
    """Extract useful keywords for simple matching.

    Args:
        text: Text to examine.

    Returns:
        Normalized keywords excluding common words.
    """    
    # Words in this set are considered too common to be useful for matching.
    stop = {"what", "when", "does", "this", "about", "every", "before"}

    return {word for word in re.findall(r"[a-z]{4,}", text.lower()) if word not in stop}


def questions_for(passage: str) -> list[str]:
    """Create likely search questions for a passage.

    Args:
        passage: Source passage to describe with questions.

    Returns:
        Generated questions linked to the passage.
    """

    lowered = passage.lower()   

    # Pick the first keyword as the main subject, or use a default if none exist.   
    subject = sorted(keywords(passage))[0]  if keywords(passage) else "this feature"

    questions = [f"What does TechNova documentation say about {subject}?"]

    # Add a specific question if the passage discusses NovaFlow and replay.
    if "novaflow" in lowered and "replay" in lowered:
        questions.append("How long can a failed NovaFlow run be replayed?")

    # Add a specific question if the passage discusses NovaDesk and exports.
    if "novadesk" in lowered and "export" in lowered:
        questions.append("How long are NovaDesk exports retained?")

    # Add a specific question if the passage discusses NovaSecure and logs.
    if "novasecure" in lowered and "logs" in lowered:
        questions.append("How long are NovaSecure security logs retained?")

    # If the passage contains timing-related words, add a frequency/duration question.
    if re.search(r"\b(every|daily|year|month|minute|hour)\b", lowered):
        questions.append("How often or for how long does this process apply?")

    # If retries are mentioned, add a question about failure behavior.
    if "retry" in lowered:
        questions.append("What happens when a document fails?")

    return questions


def main() -> None:
    """Index generated questions and retrieve their source."""

    # Store the original passages separately from their generated questions.
    store, index = {}, []

    # Process each passage and generate search questions from it.
    for passage in load_passages():

        # Create a consistent ID for the passage and store the original text.
        doc_id = uuid.uuid5(uuid.NAMESPACE_DNS, passage).hex[:8]
        store[doc_id] = passage

        # Add each generated question to the index and link it to its source passage.
        index.extend({"doc_id": doc_id, "question": q} for q in questions_for(passage))

    # This is the user's search query.
    query = "How long can a failed NovaFlow run be replayed?"

    # Find the generated question with the most keywords in common with the query.
    best = max(index, key=lambda item: len(keywords(query) & keywords(item["question"])))

    # Show how many synthetic questions were created from the source passages.
    print(f"[index] generated {len(index)} questions for {len(store)} passages")

    # Display the user's query.
    print(f"[query] {query}")

    # Display the generated question that matched the query best.
    print(f"[synthetic match] {best['question']}")

    # Use the question's doc_id to retrieve the original source passage.
    print(f"[grounded source] {store[best['doc_id']]}")


if __name__ == "__main__":
    main()