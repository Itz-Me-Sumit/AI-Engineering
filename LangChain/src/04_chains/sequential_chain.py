"""
File: sequential_chain.py

Description
-----------
Demonstrates a Sequential Chain using the LangChain Expression Language (LCEL).

The output of one step becomes the input of the next step, allowing us
to build multi-step LLM workflows.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from llm_client import get_llm

def main() -> None:
    """Demonstrates a sequential LLM workflow."""

    llm = get_llm()

    # Step 1: Generate a short blog title
    title_prompt = PromptTemplate.from_template(
        "Generate a catchy blog title about {topic}."
    )

    # Step 2: Generate a blog outline using the title
    outline_prompt = PromptTemplate.from_template(
        """
Create a blog outline for the following title.

Title:
{title}
"""
    )

    title_chain = title_prompt | llm | StrOutputParser()
    outline_chain = outline_prompt | llm | StrOutputParser()

    topic = "Retrieval-Augmented Generation (RAG)"

    print(f"Topic:\n{topic}")


    title = title_chain.invoke({"topic": topic})

    print("Generated Title:\n")
    print(title)


    outline = outline_chain.invoke({"title": title})

    print("Generated Outline:\n")
    print(outline)


if __name__ == "__main__":
    main()