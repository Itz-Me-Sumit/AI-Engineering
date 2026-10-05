# LangChain Project Structure - File Objectives

This document describes the purpose of every module and script inside the `src` directory. It serves as a roadmap for the complete LangChain learning journey.

---

# 01_llms

### openai_chat_model.py

Demonstrates how to create and interact with OpenAI chat models using LangChain.

### gemini_chat_model.py

Demonstrates how to create and interact with Google's Gemini chat models using LangChain.

### anthropic_chat_model.py

Demonstrates how to use Anthropic Claude models through LangChain.

### local_models.py

Shows how to work with locally hosted language models such as Ollama instead of cloud-based APIs.

### model_parameters.py

Explains the commonly used LLM parameters such as Temperature, Max Tokens, Top-P, Frequency Penalty, Presence Penalty and Stop Sequences, along with their effect on model behavior.

---

# 02_prompts

### src/02_prompts/prompt_template.py
Introduces PromptTemplate and demonstrates how to create reusable prompts with dynamic variables.

### src/02_prompts/chat_prompt_template.py
Explains ChatPromptTemplate and how to structure prompts using System, Human and AI messages.

### src/02_prompts/one_shot_prompt.py
Demonstrates One-Shot Prompting where the model is guided using a single example.

### src/02_prompts/few_shot_prompt.py
Demonstrates Few-Shot Prompting by providing multiple examples before asking the model to perform a task.

### src/02_prompts/chain_of_thought.py
Introduces Chain-of-Thought Prompting and explains how reasoning improves complex problem solving.

### src/02_prompts/partial_prompt.py
Shows how to partially fill prompt variables while leaving the remaining values dynamic.

### src/02_prompts/messages_placeholder.py
Demonstrates how to insert conversation history dynamically into ChatPromptTemplate.

---

# 03_output_parsers

### structured_output.py

Introduces Structured Output and demonstrates how LLM responses can follow predefined schemas.

### pydantic_parser.py

Shows how to validate and parse LLM outputs using Pydantic models.

### json_output_parser.py

Demonstrates how to generate and parse JSON responses from an LLM.

### csv_output_parser.py

Shows how structured tabular information can be generated and parsed as CSV.

### output_fixing_parser.py

Demonstrates how malformed model outputs can be automatically corrected before parsing.

---

# 04_chains

### sequential_chain.py

Demonstrates workflows where multiple LangChain components execute one after another.

### parallel_chain.py

Shows how multiple tasks can execute simultaneously using parallel execution.

### router_chain.py

Demonstrates how different inputs can be routed to different prompts or workflows.

### custom_chain.py

Builds a custom multi-step workflow by combining multiple LangChain components together.

---

# 05_memory

### chat_history.py

Introduces chat message history and explains how conversation messages are stored.

### conversation_buffer_memory.py

Demonstrates memory that stores the complete conversation.

### conversation_buffer_window.py

Shows how only the most recent conversation messages are retained.

### conversation_token_buffer.py

Demonstrates token-based memory management where history is limited using token count instead of message count.

### conversation_summary_memory.py

Shows how older conversations are summarized to reduce token usage while preserving context.

---

# 06_runnables

### runnable_sequence.py

Introduces RunnableSequence for building sequential LangChain pipelines.

### runnable_parallel.py

Demonstrates RunnableParallel for executing multiple branches simultaneously.

### runnable_lambda.py

Shows how ordinary Python functions can become LangChain Runnables.

### runnable_branch.py

Demonstrates conditional execution where different workflows run based on input conditions.

### runnable_passthrough.py

Shows how original inputs can be passed through a pipeline while additional processing is performed.

---

# 07_document_loaders
src/07_document_loaders/directory_loader.py
### text_loader.py

Demonstrates loading plain text documents into LangChain.

### pdf_loader.py

Shows how to read PDF documents for RAG applications.

### csv_loader.py

Demonstrates loading structured CSV data.

### web_loader.py

Shows how web pages can be loaded as LangChain documents.

### directory_loader.py

Demonstrates loading multiple documents automatically from a directory.

---

# 08_text_splitters

### recursive_splitter.py

Introduces RecursiveCharacterTextSplitter and explains why it is the most commonly used splitter.

### character_splitter.py

Demonstrates character-based chunking.

### token_splitter.py

Shows token-aware chunking based on LLM context windows.

### markdown_splitter.py

Demonstrates splitting Markdown documents while preserving document structure.

---
src/09_embeddings_vectorstores/similarity_search.py
# 09_embeddings_vectorstores

### embeddings.py

Introduces embeddings and demonstrates how text is converted into vector representations.

### chroma_vectorstore.py

Shows how to create and query a Chroma vector database.

### faiss_vectorstore.py

Demonstrates local vector storage and similarity search using FAISS.

### similarity_search.py

Explains similarity search and demonstrates retrieving the most semantically relevant document chunks.

---

# 10_retrievers
src/10_retrievers/parent_document_retriever.py
### vector_retriever.py

Introduces the basic vector store retriever used in most RAG applications.

### mmr_retriever.py

Demonstrates Maximum Marginal Relevance retrieval for improving result diversity.

### multi_query_retriever.py

Shows how multiple automatically generated search queries improve document retrieval.

### contextual_compression.py

Demonstrates reducing retrieved content by keeping only the most relevant information.

### parent_document_retriever.py

Shows how retrieval occurs on smaller chunks while returning larger parent documents for improved context.

---

# 11_tool_calling

### basic_tool.py

Introduces the concept of tools and demonstrates creating simple callable tools.

### tool_decorator.py

Shows how Python functions can be converted into LangChain tools using decorators.

### structured_tool.py

Demonstrates creating tools with structured and validated input parameters.

### tool_binding.py

Shows how tools are attached to an LLM so the model can decide when to invoke them.

---

# 12_projects

### Project Folder

Contains complete end-to-end applications that combine multiple LangChain concepts learned throughout the course, such as chatbots, RAG systems, document question answering, and tool-calling assistants.
