"""
File: runnable_lambda.py

Description
-----------
Demonstrates RunnableLambda.

RunnableLambda allows ordinary Python functions to behave as LangChain
Runnables, making it easy to integrate custom business logic into an
LCEL pipeline.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add project root
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.runnables import RunnableLambda

from utils.helpers import print_separator, print_title


def to_uppercase(text: str) -> str:
    """Converts text to uppercase."""
    return text.upper()


def count_words(text: str) -> str:
    """Returns the word count."""
    return f"Total Words: {len(text.split())}"


def main() -> None:
    """Demonstrates RunnableLambda."""

    print_title("Runnable Lambda")

    uppercase = RunnableLambda(to_uppercase)
    word_counter = RunnableLambda(count_words)

    text = "LangChain makes it easy to build LLM applications."

    print("Original Text:\n")
    print(text)

    print_separator()

    print("Uppercase:\n")
    print(uppercase.invoke(text))

    print_separator()

    print("Word Count:\n")
    print(word_counter.invoke(text))


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# RunnableLambda converts a normal Python function into a LangChain Runnable.
#
# This allows custom Python logic to become part of an LCEL pipeline.
#
# Example:
#
# User Input
#      ↓
# RunnableLambda
#      ↓
# Custom Python Function
# =============================================================================