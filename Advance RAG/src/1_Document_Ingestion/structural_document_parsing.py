from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

DOC_DIR = ROOT / "data" / "input" / "documents"

FALLBACK = """# NovaFlow
TechNova NovaFlow is a workflow automation platform.
## Deployment
NovaFlow runs in private cloud or on premises.
### Requirements
Deployments require Python 3.11 and a vector database.
## Security
Role-based access limits collections by team.
"""

def load_markdown() -> tuple[str , str]:
    path = DOC_DIR / "products_and_pricing.md"
    if path.exists():
        return path.read_text(encoding = "utf-8" , errors="ignore") , path.name
    return FALLBACK , "inline-technova.md"

def parse_sections(text) -> list[dict]:
    """Split Markdown into sections with heading paths.

    Args:
        text: Markdown text to parse.

    Returns:
        Section records containing paths and body text.
    """
    headings : list[str] = []
    sections : list[str] = []
    body : list[dict] = []

    def emit()->None:
        """ Save the current Section and clear it's body """
        content = "\n".join(body).strip()
        if content:
            sections.append(
                {
                    "path" : " > ".join(headings) or "Document" , 
                    "text" : content
                }
            )
        body.clear()


    for line in text.splitlines():
        if line.startswith("#") and line.lstrip("#").startswith(" "):
            emit()

            level = len(line) - len(line.lstrip("#"))
            title = line[level:].strip()
            headings[level - 1 : ] = [title]

        else:
            body.append(line)

    emit()
    return sections

def main():
    text , source = load_markdown()
    print(f"[Load] ->>  {source}")
    sections = parse_sections(text)
    print(f"[parse] emitted {len(sections)} structural sections.")

    for index , section in enumerate(sections , start = 1):
        preview = section["text"].replace("\n" , " ")[:90]
        print(f"{index}. {section["path"]}\n     {preview}")


if __name__ == "__main__":
    main()