"""
Basic RAG searches every small chunk in one flat collection.
Broad questions may then retrieve details without the overview that frames them.
The cause is treating document, section, and paragraph levels as equivalent.
Hierarchical indexing stores searchable summaries at several granularities.
This tutorial builds document, section, and detail nodes for TechNova content.
Queries first select a section summary, then search only its detail children.
This coarse-to-fine path reduces noise and makes retrieval decisions visible.
Parent identifiers preserve lineage for citations and context expansion.
Use hierarchical indexes for long manuals and naturally nested knowledge.
Production summaries may use an LLM, while hierarchy should remain deterministic.
The demonstration uses local keyword overlap and no credentials.
"""

from pathlib import Path
import re
import sys
import uuid

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

DOC_DIR = ROOT / "data" / "input" / "documents"

FALLBACK = """# TechNova Products
## NovaFlow
NovaFlow automates approvals and operational workflows.
Failed runs can be replayed for fourteen days.
## NovaSecure
NovaSecure automates access reviews and evidence collection.
Security logs are retained for 400 days.
## NovaDesk
NovaDesk provides customer support workspaces.
Exports are retained for seven days."""


def load_text() -> str:
    """Load Markdown from disk or use the sample.

    Returns:
        Markdown text for the indexing example.
    """
    path = DOC_DIR / "products_and_pricing.md"
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else FALLBACK


def tokens(text: str) -> set[str]:
    """Extract unique meaningful words from text.

    Args:
        text: Text to tokenize.

    Returns:
        Normalized words found in the text.
    """
    return set(re.findall(r"[a-z]{3,}", text.lower()))


def build_tree(text: str) -> dict:
    """Build document, section, and paragraph index levels.

    Args:
        text: Heading-based Markdown to organize.

    Returns:
        A document tree with summaries and identifiers.
    """

    # Create the top-level document and temporary containers for sections
    # and the paragraph currently being collected.
    document = {"id": "", "title": "Document", "summary": "", "sections": []}
    sections, current, paragraph = [], None, []

    def flush_paragraph() -> None:
        """Attach the current paragraph to its section."""

        # Save the collected paragraph under the current section.
        # " ".join() combines multiple lines into one paragraph.
        if current is not None and paragraph:
            current["children"].append({"id": "", "parent_id": "", "text": " ".join(paragraph)})
            paragraph.clear()

    # Read the Markdown document one line at a time.
    for line in text.splitlines():

        # "# " represents the main document title.
        if line.startswith("# "):
            flush_paragraph()
            document["title"] = line[2:].strip()

        # "## " represents a section inside the document.
        elif line.startswith("## "):
            flush_paragraph()
            current = {"title": line[3:].strip(), "children": []}
            sections.append(current)

        # A blank line means the current paragraph is complete.
        elif not line.strip():
            flush_paragraph()

        # Regular text belongs to the current section's paragraph.
        elif not line.startswith("#") and current:
            paragraph.append(line.strip())

    # Save the final paragraph because there may be no blank line at the end.
    flush_paragraph()

    # Create a stable ID for the document based on its title.
    document["id"] = uuid.uuid5(uuid.NAMESPACE_URL, document["title"]).hex[:8]

    # Add IDs and parent relationships to every section.
    for section in sections:
        section["id"] = uuid.uuid5(
            uuid.NAMESPACE_URL, f"{document['id']}:{section['title']}"
        ).hex[:8]
        section["parent_id"] = document["id"]

        # Add IDs and parent IDs to each paragraph within the section.
        for position, child in enumerate(section["children"]):
            child["id"] = uuid.uuid5(
                uuid.NAMESPACE_URL, f"{section['id']}:{position}:{child['text']}"
            ).hex[:8]
            child["parent_id"] = section["id"]

        # Create a simple summary by combining all paragraphs in the section.
        section["summary"] = f"{section['title']}: " + " ".join(
            child["text"] for child in section["children"]
        )

    # Attach all sections to the document.
    document["sections"] = sections

    # Create a document-level summary containing the names of its sections.
    document["summary"] = (
        f"{document['title']} contains sections: "
        + ", ".join(section["title"] for section in sections)
    )

    return document


def main() -> None:
    """Build the hierarchy and demonstrate coarse-to-fine search."""

    # Build the document hierarchy and get its sections.
    document = build_tree(load_text())
    sections = document["sections"]

    # This is the question we want to search for.
    query = "What does the NovaSecure plan include?"

    # Display the document-level summary.
    print(f"[document] {document['summary']}")

    # Stop if the document doesn't contain any level-two sections.
    if not sections:
        print("[empty] No level-two sections found; use a heading-aware source or fallback.")
        return

    # First find the section whose summary has the most words in common with the query.
    # This is the "coarse" search: search sections before searching individual paragraphs.
    section = max(sections, key=lambda item: len(tokens(query) & tokens(item["summary"])))

    # Stop if the selected section doesn't contain any paragraphs.
    if not section["children"]:
        print(f"[empty] Section {section['title']} has no detail paragraphs.")
        return

    # Now search only inside the selected section to find the best matching paragraph.
    # This is the "fine" search: search the smaller details after finding the right section.
    detail = max(section["children"], key=lambda child: len(tokens(query) & tokens(child["text"])))

    # Display how many sections and detail paragraphs were indexed.
    print(f"[index] {len(sections)} sections, {sum(len(s['children']) for s in sections)} details")

    # Display the search query.
    print(f"[query] {query}")

    # Show the section selected during the coarse search.
    print(f"[level 1] selected section: {section['title']} ({section['id']})")

    # Show the paragraph selected during the fine search.
    print(f"[level 2] selected detail: {detail['text']} ({detail['id']})")

    # Display the complete parent-child path from document to paragraph.
    print(f"[lineage] {document['id']} -> {section['id']} -> {detail['id']}")

    # Show a citation-style reference pointing to the exact retrieved detail.
    print(f"[citation] {document['title']} > {section['title']} [{detail['id']}]")

    # Display the complete section so the retrieved detail can be understood in context.
    print(f"[expanded parent] {section['summary']}")


if __name__ == "__main__":
    main()