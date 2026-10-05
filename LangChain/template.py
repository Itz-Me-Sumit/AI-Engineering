import os
from pathlib import Path


# ==========================================================
# Files and Folders
# ==========================================================

list_of_files = [

    # Root Files
    f".env",
    f".gitignore",
    f"README.md",
    f"requirements.txt",
    f"config.json",
    f"llm_client.py",
    f"__init__.py",

    # Data
    f"data/input/.gitkeep",
    f"data/input/sample.txt",
    f"data/input/sample.pdf",
    f"data/input/employees.csv",
    f"data/input/company_overview.txt",
    f"data/input/rag_notes.txt",
    f"data/input/langchain_notes.txt",
    f"data/input/langchain_notes.md",

    f"data/output/.gitkeep",

    # Utils
    f"utils/__init__.py",
    f"utils/helpers.py",
    f"utils/logger.py",
    f"utils/file_loader.py",
    f"utils/common.py",

    # Src Root
    f"src/__init__.py",

    # ======================================================
    # 01 LLMs
    # ======================================================

    f"src/01_llms/__init__.py",
    f"src/01_llms/openai_chat_model.py",
    f"src/01_llms/gemini_chat_model.py",
    f"src/01_llms/anthropic_chat_model.py",
    f"src/01_llms/local_models.py",
    f"src/01_llms/model_parameters.py",
    f"src/01_llms/__init__.py",

    # ======================================================
    # 02 Prompts
    # ======================================================

    f"src/02_prompts/__init__.py",
    f"src/02_prompts/prompt_template.py",
    f"src/02_prompts/chat_prompt_template.py",
    f"src/02_prompts/one_shot_prompt.py",
    f"src/02_prompts/few_shot_prompt.py",
    f"src/02_prompts/chain_of_thought.py",
    f"src/02_prompts/partial_prompt.py",
    f"src/02_prompts/messages_placeholder.py",
    f"src/02_prompts/__init__.py",

    # ======================================================
    # 03 Output Parsers
    # ======================================================

   f"src/03_output_parsers/__init__.py",
   f"src/03_output_parsers/structured_output.py",
   f"src/03_output_parsers/pydantic_parser.py",
   f"src/03_output_parsers/json_output_parser.py",
   f"src/03_output_parsers/csv_output_parser.py",
   f"src/03_output_parsers/output_fixing_parser.py",
   f"src/03_output_parsers/__init__.py",

    # ======================================================
    # 04 Chains
    # ======================================================

   f"src/04_chains/__init__.py",
   f"src/04_chains/sequential_chain.py",
   f"src/04_chains/parallel_chain.py",
   f"src/04_chains/router_chain.py",
   f"src/04_chains/custom_chain.py",
   f"src/04_chains/__init__.py",

    # ======================================================
    # 05 Memory
    # ======================================================

   f"src/05_memory/__init__.py",
   f"src/05_memory/chat_history.py",
   f"src/05_memory/conversation_buffer_memory.py",
   f"src/05_memory/conversation_buffer_window.py",
   f"src/05_memory/conversation_token_buffer.py",
   f"src/05_memory/conversation_summary_memory.py",
   f"src/05_memory/__init__.py",

    # ======================================================
    # 06 Runnables
    # ======================================================

    f"src/06_runnables/__init__.py",
    f"src/06_runnables/runnable_sequence.py",
    f"src/06_runnables/runnable_parallel.py",
    f"src/06_runnables/runnable_lambda.py",
    f"src/06_runnables/runnable_branch.py",
    f"src/06_runnables/runnable_passthrough.py",
    f"src/06_runnables/__init__.py",

    # ======================================================
    # 07 Document Loaders
    # ======================================================

    f"src/07_document_loaders/__init__.py",
    f"src/07_document_loaders/text_loader.py",
    f"src/07_document_loaders/pdf_loader.py",
    f"src/07_document_loaders/csv_loader.py",
    f"src/07_document_loaders/web_loader.py",
    f"src/07_document_loaders/directory_loader.py",
    f"src/07_document_loaders/__init__.py",

    # ======================================================
    # 08 Text Splitters
    # ======================================================

    f"src/08_text_splitters/__init__.py",
    f"src/08_text_splitters/recursive_splitter.py",
    f"src/08_text_splitters/character_splitter.py",
    f"src/08_text_splitters/token_splitter.py",
    f"src/08_text_splitters/markdown_splitter.py",
    f"src/08_text_splitters/__init__.py",

    # ======================================================
    # 09 Embeddings & VectorStores
    # ======================================================

    f"src/09_embeddings_vectorstores/__init__.py",
    f"src/09_embeddings_vectorstores/embeddings.py",
    f"src/09_embeddings_vectorstores/chroma_vectorstore.py",
    f"src/09_embeddings_vectorstores/faiss_vectorstore.py",
    f"src/09_embeddings_vectorstores/similarity_search.py",
    f"src/09_embeddings_vectorstores/__init__.py",

    # ======================================================
    # 10 Retrievers
    # ======================================================

    f"src/10_retrievers/__init__.py",
    f"src/10_retrievers/vector_retriever.py",
    f"src/10_retrievers/mmr_retriever.py",
    f"src/10_retrievers/multi_query_retriever.py",
    f"src/10_retrievers/contextual_compression.py",
    f"src/10_retrievers/parent_document_retriever.py",
    f"src/10_retrievers/__init__.py",

    # ======================================================
    # 11 Tool Calling
    # ======================================================

    f"src/11_tool_calling/__init__.py",
    f"src/11_tool_calling/basic_tool.py",
    f"src/11_tool_calling/tool_decorator.py",
    f"src/11_tool_calling/structured_tool.py",
    f"src/11_tool_calling/tool_binding.py",
    f"src/11_tool_calling/__init__.py",

    # ======================================================
    # 12 Projects
    # ======================================================

    f"src/12_projects/__init__.py",
    f"src/12_projects/.gitkeep",

]

# ==========================================================
# Create Structure
# ==========================================================

for filepath in list_of_files:

    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w", encoding="utf-8") as f:
            pass

print("=" * 60)
print(f"Project created successfully!")
print("=" * 60)