"""
Basic RAG often extracts a PDF as one flat stream of text.
That loses page boundaries, tables, headings, and reading order.
The cause is that PDFs store positioned drawing commands, not paragraphs.
Advanced PDF parsing keeps page-level provenance and layout hints.
This tutorial reads every available TechNova PDF with PyMuPDF.
It detects likely headings and table-like rows using simple heuristics.
The resulting records can be chunked without discarding page metadata.
Useful stage output makes extraction quality easy to inspect.
Use this technique for reports, manuals, and policy documents.
Scanned PDFs additionally require an OCR tool such as Tesseract.
The local demonstration needs no API key.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
# Add the project root to Python's import path
# This allows Python to find modules/packages in the project
sys.path.insert(0, str(ROOT))

PDF_DIR = ROOT / "data" / "input" / "pdfs"


def classify_line(line: str) -> str:
    """Classify an extracted PDF line by its visible structure.
    Args:
        line: Text line read from a PDF page.
    Returns:
        A label such as heading, table-row, or paragraph.
    """
    words = line.split()
    if len(words) <= 10 and (line.isupper() or line.endswith(":")):
        return "heading"
    
    # r"\s{2,}|\|" means:
    #   \s{2,}  -> find 2 or more whitespace characters (spaces/tabs/newlines)
    #   |       -> OR
    #   \|      -> find a literal pipe character |
    if len(re.findall(r"\s{2,}|\|", line)) >= 2:
        return "table-row"
    return "paragraph"


def parse_pdf(path: Path) -> list[dict]:
    """Extract structured text blocks from a PDF.

    Args:
        path: PDF file to read.

    Returns:
        Records containing each block's text and location.
    """
    try:
        import pymupdf
    except ImportError as exc:
        raise RuntimeError("Install PDF support with: pip install pymupdf") from exc

    records = []
    with pymupdf.open(path) as pdf:
        for page_number, page in enumerate(pdf, 1):
            blocks = page.get_text("blocks", sort=True)
            for block_number, block in enumerate(blocks, 1):
                raw_text = block[4].strip()
                # In PyMuPDF, each block usually looks like: (x0, y0, x1, y1, text, ...)
                if raw_text:
                    # Layout classification must see raw spacing/newlines. Normalizing
                    # first would erase the column gaps used by the table heuristic.
                    raw_lines = [line for line in raw_text.splitlines() if line.strip()]
                    kind = (
                        "table-row"
                        if any(classify_line(line) == "table-row" for line in raw_lines)
                        else classify_line(raw_text)
                    )
                    records.append(
                        {
                            "source": path.name,
                            "page": page_number,
                            "block": block_number,
                            "kind": kind,
                            "text": " ".join(raw_text.split()),
                        }
                    )
    return records


def main() -> None:
    """Parse the available PDFs and print a short preview."""
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {PDF_DIR}. Add a TechNova PDF and rerun.")
        return
    for pdf in pdfs:
        print(f"\n[load] {pdf.name}")
        try:
            records = parse_pdf(pdf)
        except RuntimeError as error:
            print(f"[dependency] {error}")
            return
        pages = {item["page"] for item in records}
        print(f"[parsed] {len(records)} blocks across {len(pages)} pages")
        for item in records[:6]:
            print(f"  p{item['page']:02} {item['kind']:9} | {item['text'][:90]}")


if __name__ == "__main__":
    main()