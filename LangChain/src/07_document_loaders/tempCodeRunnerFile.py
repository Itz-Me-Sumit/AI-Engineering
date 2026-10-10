import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))


from langchain_community.document_loaders import WebBaseLoader

def main():

    loader = WebBaseLoader(
        web_path=(
            "https://python.langchain.com/docs/introduction/",
        )
    )
    documents = loader.load()

    print(f"Total Documents Loaded : {len(documents)}")

    print(f"First Document : \n{documents[0]}")


if __name__ == "__main__":
    main()