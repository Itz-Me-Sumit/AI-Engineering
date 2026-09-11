from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path = "Social_Network_Adventure.csv")

docs = loader.load()

print(docs)