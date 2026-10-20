import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from llm_client import get_llm

def main():
    
    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"

    embedding_model = OpenAIEmbeddings(
        model = "openai/text-embedding-3-small",
        base_url="https://openrouter.ai/api/v1",
        api_key = os.getenv("OPENROUTER_API_KEY"),
        check_embedding_ctx_length=False,
    )



    loader = TextLoader(file_path)
    documents = loader.load()

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 10,
    )
    chunks = recursive_splitter.split_documents(documents)

    faiss_vector_store = FAISS.from_documents(
        documents = chunks,
        embedding = embedding_model
    )

    retriever_obj = faiss_vector_store.as_retriever(
        search_kwargs = {
            "k" : 3
        },
    )

    retriever = MultiQueryRetriever.from_llm(
        retriever = retriever_obj,
        llm = get_llm(),
        include_original = True
    )

    query = "What is Artificial Intelligence"

    docs = retriever.invoke(query)

    for idx , doc in enumerate(docs , start = 1):
        print(f"\nRetrieved Doc {idx} -> {doc.page_content}\n")

if __name__ == "__main__":
    main()