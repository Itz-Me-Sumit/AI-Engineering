import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter


def main():

    file_path = PROJECT_ROOT / "data" / "input" / "langchain_notes.md"

    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    print(f"Total Documents Loaded: {len(documents)}\n")

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3")
        ]
    )

    chunks = markdown_splitter.split_text(documents[0].page_content)

    print(f"Total Chunks: {len(chunks)}\n")

    for idx, chunk in enumerate(chunks, start=1):
        print(f"Chunk {idx}")
        print(f"Content:\n{chunk.page_content}")
        print(f"Metadata: {chunk.metadata}")
        print(f"Total Characters: {len(chunk.page_content)}")
        print("-" * 80)


if __name__ == "__main__":
    main()