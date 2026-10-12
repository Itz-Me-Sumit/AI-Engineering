import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain_chroma import chroma

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

    vector_store = FAISS.from_documents(
        documents = chunks,
        embedding = embedding_model,
    )

    query = "What is RAG"

    results = vector_store.similarity_search(
        query ,
        k = 3
    )

    for idx , result in enumerate(results , start = 1):
        print(f"\nResult {idx} -> {result} \n")



if __name__ == "__main__":
    main()