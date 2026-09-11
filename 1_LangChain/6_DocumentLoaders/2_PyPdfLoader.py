from langchain_community.document_loaders import PyPDFLoader

pdf_loader = PyPDFLoader('Adventure.pdf')

docs = pdf_loader.load()

print(docs[0])
print("\n\n")
print("page content")
print()
print(docs[0].page_content)
print("metadata")
print()
print(docs[0].metadata)