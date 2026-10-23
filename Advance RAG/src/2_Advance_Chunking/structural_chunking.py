import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
DOC_DIR = ROOT / "data" / "input" / "documents"


FALLBACK = """# NovaFlow
NovaFlow automates approvals and operational workflows.
## Deployment
Install the service in a private cloud.

Configure one workflow workspace per business unit. Restart workers after changing settings.
## Security
NovaSecure roles restrict workflow administration. Audit events are retained.
"""


def load_markdown() -> str:
    return FALLBACK

def structural_chunks(text: str , max_words: int = 28) -> list[dict]:
    """Create size-limited chunks that preserve headings.

    Args:
        text: Markdown text to split.
        max_words: Maximum words allowed in each chunk.

    Returns:
        Chunks with their section breadcrumbs.
    """


    path: list[str] = []
    # keeps a track of current hierarchy
    # Example : ["Introduction" , "RAG" , "Chunking"]

    sections: list[
        tuple[
            str,
            list[str]
        ]
    ] = []
    # stores completed sections as:
    #   ("Introduction > RAG" , ["Paragraph1" , "Paragraph2" , ... ,])

    paragraphs: list[str] = []
    # Stores complete paragraph temporarily that belong to the current section

    paragraph_lines: list[str] = []
    # This temporarily collects individual lines that together form one paragraph
    
    def SaveAndFlush_paragraph():
        """ save the collected lines in one paragraph and clear it's content  """
        if paragraph_lines:
            paragraphs.append(" ".join(paragraph_lines))
            paragraph_lines.clear()

    def SaveAndFlush_section():

        """ Save the current section and clear it's paragraphs """
        SaveAndFlush_paragraph()

        if paragraphs:
            sections.append(
                (
                    " > ".join(path) or "Document",
                    paragraphs.copy()
                )
            )
            paragraphs.clear()


    for line in text.splitlines():
        if line.startswith("#"):
            SaveAndFlush_section()

            level = len(line) - len(line.lstrip("#"))

            path[level-1:] = [line[level:].strip()]

        elif not line.strip():
            SaveAndFlush_paragraph()

        elif line.strip():
            paragraph_lines.append(line.strip())

    SaveAndFlush_section()

    chunks = []

    for breadcrumb , paragraphs in sections:
        current: list[str] = []
        current_words = 0

        for paragraph in paragraphs:
            words = paragraph.split()

            # If a paragraph is larger then max_words then split it into smaller pieces of at most "max_words"
            pieces = [
                " ".join(words[i : i+max_words])
                for i in range(0 , len(words) , max_words)    
            ]
            for piece in pieces:
                piece_words = len(piece.split())
                if current and (current_words+piece_words) > max_words:
                    chunks.append(
                        {
                            "section":breadcrumb , 
                            "text" : "\n\n".join(current)
                        }
                    )
                    current = []
                    current_words = 0

                current.append(piece)
                current_words+=piece_words

            if current:
                chunks.append(
                    {
                        "section":breadcrumb,
                        "text" : "\n\n".join(current)
                    }
                )
    return chunks

def main():
    text = load_markdown()
    chunks = structural_chunks(text)

    print(f"\n\nTotal Chunks created : {len(chunks)}\n")
    for idx , chunk in enumerate(chunks , start = 1):
        print(f"chunk {idx} : {chunk}\n\n")


if __name__ == "__main__":
    main()