import os
import sys
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

def main():

    file_path = PROJECT_ROOT / "data" / "input" / "sample.pdf"
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    token_splitter = TokenTextSplitter(
        chunk_size = 100,
        chunk_overlap = 20
    )
    chunks = token_splitter.split_documents(documents)

    embedding_model = OpenAIEmbeddings(
        model = "openai/text-embedding-3-small",
        base_url="https://openrouter.ai/api/v1",
        api_key = os.getenv("OPENROUTER_API_KEY"),
        check_embedding_ctx_length=False,
    )
    chroma_db_path = PROJECT_ROOT / "data" / "chroma_db"

    if chroma_db_path.exists():
        shutil.rmtree(chroma_db_path)

    print("Adding documents to Chroma Vector Store...")
    vector_store = Chroma.from_documents(
        documents = chunks,
        embedding = embedding_model,
        collection_name = "langchain_chroma_db",
        persist_directory = str(chroma_db_path)
    )
    print("Added to chroma Vector Store !!")

    query = "What is Generative AI"

    results = vector_store.similarity_search(
        query,
        k = 3
    )

    for idx , result in enumerate(results , start = 1):
        print(f"\nResult : {idx} -> {result}\n\n")


if __name__ == "__main__":
    main()