# AI Engineer

A structured, hands-on roadmap to becoming an AI Engineer. This repository is the entry point to three focused repositories that together cover the full journey from calling an LLM for the first time to building production-grade agentic and retrieval systems.

Each repository is self-contained, code-first, and organized so that every concept lives in its own runnable file.

---

## Learning Path

GenAI (foundations)  ->  Advanced RAG (knowledge systems)  ->  Agentic AI (autonomous systems)

You can follow the path in order or jump into any repository directly.

---

## Repositories

### 1. GenAI
Link: https://github.com/Itz-Me-Sumit/GenAI

The foundation layer. Covers everything you need to build LLM applications with LangChain.

- LLMs: using different model providers through a unified interface
- Prompt engineering: templates, few-shot, chain-of-thought, partial prompts
- Output parsers: structured, JSON, CSV, Pydantic, output-fixing
- Chains: sequential, parallel, router and custom chains
- Memory: chat history, buffer, window, summary and token-based strategies
- Runnables (LCEL): branch, lambda, parallel, passthrough, sequence
- RAG basics: document loaders, text splitters and retrievers

Best for: anyone starting with LLM application development.

---

### 2. Advanced RAG
Link: https://github.com/Itz-Me-Sumit/Advance-RAG

Goes beyond basic retrieval. Focuses on making RAG systems accurate, scalable and production-ready.

- Advanced chunking and indexing strategies
- Hybrid search (dense + sparse) and re-ranking
- Query transformation and multi-query retrieval
- Contextual compression and parent-document retrieval
- Evaluation of RAG pipelines (retrieval and generation quality)
- Optimization for latency, cost and relevance

Best for: engineers who want reliable question-answering over private data.

---

### 3. Agentic AI
Link: https://github.com/Itz-Me-Sumit/Agentic-AI

Building systems that reason, use tools and act autonomously.

- LangGraph: stateful, graph-based agent workflows
- Tool calling and custom tools
- Model Context Protocol (MCP): connecting agents to external tools and data
- Multi-agent collaboration patterns
- Human-in-the-loop, persistence and checkpointing
- Deployment of agent-based applications

Best for: engineers building assistants, copilots and workflow automation.

---

## Tech Stack

- Language: Python
- Frameworks: LangChain, LangGraph , Pydantic , Streamlit
- Protocols: MCP
- Vector stores: FAISS, Chroma (and others used per repo)
- LLM providers: OpenAI, Anthropic, Google, open-source models via OpenRouter / Hugging Face

---

## Getting Started

1. Clone the repository you want to explore
2. Create a virtual environment and install dependencies from its requirements.txt
3. Add your API keys in a .env file (see .env.example in each repo)
4. Run any file directly to see that concept in action

---

## Author

Sumit
GitHub: https://github.com/Itz-Me-Sumit
LinkedIn: [<your-linkedin-link>](https://www.linkedin.com/in/sumit-kumar-809687360/)

If this repository helps you, consider giving it a star.