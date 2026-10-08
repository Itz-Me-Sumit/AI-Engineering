"""
File: runnable_branch.py

Description
-----------
Demonstrates RunnableBranch.

RunnableBranch executes different workflows depending on whether a
specified condition evaluates to True or False.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add project root
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch

from llm_client import get_llm
from utils.helpers import print_separator, print_title


def main() -> None:
    """Demonstrates RunnableBranch."""

    print_title("Runnable Branch")

    llm = get_llm()

    technical_chain = (
        PromptTemplate.from_template(
            "Answer the following technical question:\n\n{query}"
        )
        | llm
        | StrOutputParser()
    )

    general_chain = (
        PromptTemplate.from_template(
            "Answer the following general question:\n\n{query}"
        )
        | llm
        | StrOutputParser()
    )

    branch = RunnableBranch(
        (
            lambda x: any(
                keyword in x["query"].lower()
                for keyword in [
                    "python",
                    "langchain",
                    "llm",
                    "rag",
                    "embedding",
                ]
            ),
            technical_chain,
        ),
        general_chain,
    )

    query = "What is Retrieval-Augmented Generation (RAG)?"

    print(f"Query:\n{query}")

    print_separator()

    response = branch.invoke({"query": query})

    print("Response:\n")
    print(response)


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# RunnableBranch allows conditional execution inside an LCEL pipeline.
#
# Based on a condition, one of multiple runnables is executed.
#
# Example:
#
# User Query
#      │
#      ▼
# Is it technical?
#      │
#   ┌──┴──┐
# Yes    No
#  │      │
# Tech  General
# Chain  Chain
# =============================================================================