import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from langchain_community.document_loaders import TextLoader


def main():

    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"

    loader = TextLoader(file_path) # TextLoader recives text file path and returns a loader object
    documents = loader.load()

    print("---" * 40)

    print(f"Total Dcouments loaded : {len(documents)}")

    print("---" * 40)

    print(f"Documents : \n{documents}")

    print("---" * 40)

    print(f"first document : \n{documents[0].page_content}")

if __name__ == "__main__":
    main()