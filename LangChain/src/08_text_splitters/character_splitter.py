import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))


from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

def main():

    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"

    loader = TextLoader(file_path)
    documents = loader.load()
    print(f"Total Documents : {len(documents)}")


    character_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 200,
        chunk_overlap = 50,
    )

    chunks = character_splitter.split_documents(documents)
    print(f"Total Chunks : {len(chunks)}")

    for idx , chunk in enumerate(chunks , start = 1):
        print(f"chunk : {idx} -> {chunk} \n{len(chunk.page_content)}\n\n\n")



if __name__ == "__main__":
    main()