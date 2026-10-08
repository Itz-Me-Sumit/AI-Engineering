"""
File: parallel_chain.py

Description
-----------
Demonstrates a Parallel Chain using LCEL.

Unlike a Sequential Chain, multiple independent tasks execute
simultaneously on the same input, making workflows faster and more
efficient.
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
from langchain_core.runnables import RunnableParallel

from llm_client import get_llm


def main() -> None:
    """Demonstrates a parallel LLM workflow."""


    llm = get_llm()

    summary_prompt = PromptTemplate.from_template(
        "Write a short summary about {topic}."
    )

    advantages_prompt = PromptTemplate.from_template(
        "List three advantages of {topic}."
    )

    applications_prompt = PromptTemplate.from_template(
        "List three real-world applications of {topic}."
    )

    parallel_chain = RunnableParallel(
        summary=summary_prompt | llm | StrOutputParser(),
        advantages=advantages_prompt | llm | StrOutputParser(),
        applications=applications_prompt | llm | StrOutputParser(),
    )

    topic = "Retrieval-Augmented Generation (RAG)"

    print(f"Topic:\n{topic}")


    result = parallel_chain.invoke({"topic": topic})

    print("Summary:\n")
    print(result["summary"])


    print("Advantages:\n")
    print(result["advantages"])


    print("Applications:\n")
    print(result["applications"])


if __name__ == "__main__":
    main()