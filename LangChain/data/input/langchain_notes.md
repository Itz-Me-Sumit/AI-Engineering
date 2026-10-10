# LangChain

LangChain is a framework for building applications powered by Large Language Models.

## Core Components

LangChain provides several important components.

### Prompt Templates

Prompt Templates help create reusable prompts with dynamic variables.

### Output Parsers

Output Parsers convert raw LLM responses into structured formats.

## RAG

Retrieval-Augmented Generation combines retrieval with language models.

### Document Loaders

Document Loaders read documents from different sources.

### Text Splitters

Text Splitters divide large documents into smaller chunks.

### Embedding Models

Embedding Models convert text into numerical vectors.

## Example Code

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

response = llm.invoke("Hello")
print(response.content)
```

## Conclusion

LangChain simplifies the development of LLM-powered applications.