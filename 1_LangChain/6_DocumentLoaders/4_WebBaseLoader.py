from langchain_community.document_loaders import WebBaseLoader

url = ""

loader = WebBaseLoader(url)

"""
loader = WebBaseLoader([url1 , url2 , url3])
"""

docs = loader.load()

print(docs[0].page_content)
