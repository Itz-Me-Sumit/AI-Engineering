import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

def main():

    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"

    text_loader = TextLoader(file_path)
    documents = text_loader.load()

    print(f"Total Documents Loaded : {len(documents)}")

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 50,
    )

    chunks = recursive_splitter.split_documents(documents)

    print(f"Chunks Created : {len(chunks)}")

    for i , chunk in enumerate(chunks , start = 1):
        print(f"Chunk : {i} -> {chunk}\nCharacters : {len(chunk.page_content)}\n\n\n")
        

if __name__ == "__main__":
    main()