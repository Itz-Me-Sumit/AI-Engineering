import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))



from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

def main():

    file_path = PROJECT_ROOT / "data" / "input" / "sample.txt"
    loader = TextLoader(file_path)
    documents = loader.load()

    recursive_loader = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 20
    )

    chunks = recursive_loader.split_documents(documents)

    texts = [chunk.page_content for chunk in chunks]

    embedding_model = OpenAIEmbeddings(
        model = "openai/text-embedding-3-small",
        base_url="https://openrouter.ai/api/v1",
        api_key = os.getenv("OPENROUTER_API_KEY"),
        check_embedding_ctx_length=False,
    )

    embeddings = embedding_model.embed_documents(texts)

    for idx , embedding in enumerate(embeddings , start = 1):
        print(f"Embedding : {idx} -> {embedding} \ntotal embedding Created : {len(embedding)}\n\n\n")




if __name__ == "__main__":
    main()