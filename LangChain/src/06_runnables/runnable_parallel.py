"""
File: runnable_parallel.py

Description
-----------
Demonstrates RunnableParallel.

RunnableParallel executes multiple independent runnables simultaneously
using the same input.
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
from utils.helpers import print_separator, print_title


def main() -> None:
    """Demonstrates RunnableParallel."""

    print_title("Runnable Parallel")

    llm = get_llm()

    summary_chain = (
        PromptTemplate.from_template(
            "Write a short summary about {topic}."
        )
        | llm
        | StrOutputParser()
    )

    advantages_chain = (
        PromptTemplate.from_template(
            "List three advantages of {topic}."
        )
        | llm
        | StrOutputParser()
    )

    applications_chain = (
        PromptTemplate.from_template(
            "List three real-world applications of {topic}."
        )
        | llm
        | StrOutputParser()
    )

    parallel_chain = RunnableParallel(
        summary=summary_chain,
        advantages=advantages_chain,
        applications=applications_chain,
    )

    topic = "Vector Databases"

    print(f"Topic:\n{topic}")

    print_separator()

    result = parallel_chain.invoke({"topic": topic})

    print("Summary:\n")
    print(result["summary"])

    print_separator()

    print("Advantages:\n")
    print(result["advantages"])

    print_separator()

    print("Applications:\n")
    print(result["applications"])


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# RunnableParallel executes multiple runnables simultaneously.
#
# Every runnable receives the same input, and the outputs are returned
# together as a dictionary.
#
# Example:
#
#                Topic
#                  │
#        ┌─────────┼─────────┐
#        ▼         ▼         ▼
#    Summary   Advantages   Applications
#        │         │         │
#        └─────────┼─────────┘
#                  ▼
#          Combined Dictionary
# =============================================================================