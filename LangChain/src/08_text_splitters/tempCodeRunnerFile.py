import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

def main():

    file_path = PROJECT_ROOT / "data" / "input" / "sample.pdf"
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    print(f"Total Documents loaded : {len(documents)}")

    token_splitter = TokenTextSplitter(
        chunk_size = 200,
        chunk_overlap = 50
    )

    chunks = token_splitter.split_documents(documents)

    print(f"Total Chunks : {len(chunks)}")

    for idx , chunk in enumerate(chunks , start = 1):
        print(f"Chunk {idx} -> {chunk}\ncharacter:{len(chunk.page_content)}\n\n\n")



if __name__ == "__main__":
    main()