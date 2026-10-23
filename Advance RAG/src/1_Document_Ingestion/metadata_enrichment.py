from datetime import datetime, timezone
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
# Add the project root to Python's import path
# This allows Python to find modules/packages in the project
sys.path.insert(0, str(ROOT))
DOC_DIR = ROOT/"data"/"input"/"documents"

FALLBACK = (
    "TechNova NovaFlow deployment guide. The platform supports private cloud "
    "installation, semantic search, and role-based access control."
)

def infer_topics(text: str) -> list[str]:
    """Find known topic words in document text.

    Args:
        text: Document text to inspect.

    Returns:
        Topic names found in the text.
    """
    vocabulary = ["security", "deployment", "cloud", "search", "api", "pricing"]    
    lowered = text.lower()
    return [topic for topic in vocabulary if topic in lowered]

def enrich(path: Path | None, text: str) -> dict:
    """Build useful metadata for a document.

    Args:
        path: Source file path, or None for the sample.
        text: Document text being described.

    Returns:
        Metadata about the source and its content.
    """
    if path:
        stat = path.stat()

        modified = datetime.fromtimestamp(stat.st_mtime, timezone.utc).date().isoformat()
        # Converts the file's last-modified timestamp into a readable date like "2026-09-25"
        source, extension = path.name, path.suffix.lower().lstrip(".")
    else: 
        modified, source, extension = "2026-09-25", "technova-novaflow.txt", "txt"

    title = re.sub(r"[-_]+", " ", Path(source).stem).title()
    # tech-nova_guide ->> "Tech Nove Guide"

    return {
        "source": source,
        "title": title,
        "format": extension,
        "modified_date": modified,
        "character_count":len(text),
        "topics": infer_topics(text),
        "organization": "TechNova",
    }

def main():
    files = sorted([*DOC_DIR.glob("*.md"), *DOC_DIR.glob("*.txt")])
    path = files[0] if files else None
    text = path.read_text(encoding = "utf-8", errors = "ignore") if path else FALLBACK
    print(f"[load] ->> {path.name if path else 'inline fallback'}")
    metadata = enrich(path, text)
    for key, value in metadata.items():
        print(f"{key:16}: {value}")

if __name__=="__main__":
    main()