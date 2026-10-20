import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from llm_client import get_llm
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor


def main():

    embedding_model = OpenAIEmbeddings(
        model = "openai/text-embedding-3-small",
        base_url="https://openrouter.ai/api/v1",
        api_key = os.getenv("OPENROUTER_API_KEY"),            
        check_embedding_ctx_length=False,
    )

    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"
    loader = TextLoader(file_path)

    print("Loading File...")
    documents = loader.load()
    print("File Loaded !!!")

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 10,
    )

    print("Splitting Documents...")
    chunks = recursive_splitter.split_documents(documents)
    print("Documents Splitted !!!")

    print("Storing Embeddings into FAISS Vector store...")
    vector_store = FAISS.from_documents(
        documents = chunks,
        embedding = embedding_model,
    )
    print("Embeddings stored !!!")

    print("Creating Retriever")
    base_retriever = vector_store.as_retriever(
        search_kwargs = {
            "k" : 2,
        }
    )

    compressor = LLMChainExtractor.from_llm(
        get_llm()
    ) 
    retriever = ContextualCompressionRetriever(
        base_retriever = base_retriever,
        base_compressor = compressor
    )
    print("Retriever Created")

    query = "Explain Artificial Intelligence"

    docs = retriever.invoke(query)

    for idx , doc in enumerate(docs , start = 1):
        print(f"\nRrtrieved {idx} -> {doc.page_content}\n")


if __name__ == "__main__":
    main()