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

def main():

    embedding_model = OpenAIEmbeddings(
        model = "openai/text-embedding-3-small",
        base_url="https://openrouter.ai/api/v1",
        api_key = os.getenv("OPENROUTER_API_KEY"),
        check_embedding_ctx_length=False,
    )

    vector_store = FAISS.from_documents(
        documents = RecursiveCharacterTextSplitter(
            chunk_size = 100,
            chunk_overlap = 20,
        ).split_documents(
            TextLoader(PROJECT_ROOT / "data" / "input" / "sample.txt").load()
        ),
        embedding = embedding_model,
    )

    retriever = vector_store.as_retriever(
        search_kwargs = {"k" : 2}
    )

    query = "what are large language models"

    docs = retriever.invoke(query)

    for idx , doc in enumerate(docs):
        print(f"\nRetireived Documents : {idx} -> {doc.page_content}\n")

if __name__ == "__main__":
    main()