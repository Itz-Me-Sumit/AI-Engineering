import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)

def main():

    path = PROJECT_ROOT / "data" / "input"

    loader = DirectoryLoader(
        path = path,
        glob = "**/*.txt",
        loader_cls = TextLoader
    )

    documents = loader.load()

    print(f"Total Documents : {len(documents)}")
    print(f"1st Docs Page Content : \n{documents[0].page_content}")
    


if __name__ == "__main__":
    main()