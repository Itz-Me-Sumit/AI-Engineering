import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))


from langchain_community.document_loaders import CSVLoader

def main():

    file_path = PROJECT_ROOT / "data" / "input" / "employees.csv"
    loader = CSVLoader(file_path)
    documents = loader.load()

    print(f"Total documents loaded : {len(documents)}")
    print(f"total documents : \n{documents}")
    print(f"1st page : \n{documents[0].page_content}\n")
    print(f"2nd page : \n{documents[1].page_content}\n")

if __name__ == "__main__":
    main()