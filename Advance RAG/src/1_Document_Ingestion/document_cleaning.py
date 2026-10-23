from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

FALLBACK = """TECHNOVA NOVAFLOW GUIDE
Page 1 of 4
TechNova's Nova-
Flow engine automates operational workflows.

Confidential - TechNova
It supports approval routing.    Teams can deploy it securely.
Page 2 of 4
"""

def load_text() -> tuple[str, str]:
    return FALLBACK, "inline-artificial-bearing-guide.txt"

def clean_document(text: str) -> str:
    """Remove common extraction noise from document text.

    Args:
        text: Raw document text to clean.

    Returns:
        Cleaned text with normalized spacing.
    """
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.fullmatch(r"(Confidential\s*-\s*)?TechNova", stripped, flags=re.I):
            # TechNova
            # Confidential - TechNova
            # confidential-technova
            continue
        if re.fullmatch(r"Page \d+ of \d+", stripped, flags=re.I):
            # Page 1 of 4
            # page 2 of 10
            continue
        lines.append(line)

    text = "\n".join(lines)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text) # Nova-\nFlow -> "NovaFlow"
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def main():
    raw, source = load_text()
    cleaned = clean_document(raw)
    print(f"[source] -> {source}")
    print(f"[before] -> {len(raw)} characters.")
    print(f"[after] -> {len(cleaned)} characters.")
    print("----------------------------------")
    print(cleaned[:350])

if __name__=="__main__":
    main()