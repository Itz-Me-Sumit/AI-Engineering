# New way to do this
"""
from langchain_core.documents import Document
with open("cricket.txt" , "r" , encoding = 'utf-8') as f:
    text = f.read()
documents = [
    Document(
        page_content = text,
        metadata = {"source" : "cricket.txt"}
    )
]
"""

from langchain_community.document_loaders import TextLoader


loader = TextLoader("cricket.txt" , encoding = "utf-8")
docs = loader.load()

print(docs)