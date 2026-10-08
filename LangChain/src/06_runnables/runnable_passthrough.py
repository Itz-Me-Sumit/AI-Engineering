"""
File: runnable_passthrough.py

Description
-----------
Demonstrates RunnablePassthrough.

RunnablePassthrough forwards the original input while allowing additional
processing to happen in parallel. This is useful when you want to preserve
the original data along with newly generated outputs.
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
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from llm_client import get_llm
from utils.helpers import print_separator, print_title


def main() -> None:
    """Demonstrates RunnablePassthrough."""

    print_title("Runnable Passthrough")

    llm = get_llm()

    summary_chain = (
        PromptTemplate.from_template(
            "Write a short summary about {topic}."
        )
        | llm
        | StrOutputParser()
    )

    pipeline = RunnableParallel(
        original_input=RunnablePassthrough(),
        summary=summary_chain,
    )

    topic = "Large Language Models"

    print(f"Input Topic:\n{topic}")

    print_separator()

    result = pipeline.invoke({"topic": topic})

    print("Original Input:\n")
    print(result["original_input"])

    print_separator()

    print("Generated Summary:\n")
    print(result["summary"])


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# RunnablePassthrough forwards the original input without modifying it.
#
# It is useful when you want to keep the original input while generating
# additional outputs in parallel.
#
# Example:
#
#                 User Input
#                     │
#         ┌───────────┴───────────┐
#         ▼                       ▼
# RunnablePassthrough      Summary Chain
#         │                       │
#         └───────────┬───────────┘
#                     ▼
#              Combined Output
# =============================================================================