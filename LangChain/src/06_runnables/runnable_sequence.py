"""
File: runnable_sequence.py

Description
-----------
Demonstrates RunnableSequence.

RunnableSequence allows multiple LangChain components to execute one
after another, where the output of one component automatically becomes
the input of the next component.
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
from utils.helpers import print_separator, print_title


def main() -> None:
    """Demonstrates RunnableSequence."""

    print_title("Runnable Sequence")

    llm = get_llm()

    prompt = PromptTemplate.from_template(
        "Explain {topic} in less than 100 words."
    )

    sequence = prompt | llm | StrOutputParser()

    topic = "Vector Databases"

    print(f"Topic:\n{topic}")

    print_separator()

    response = sequence.invoke({"topic": topic})

    print("Response:\n")
    print(response)


if __name__ == "__main__":
    main()


# =============================================================================
# Concept Summary
#
# RunnableSequence executes multiple runnables one after another.
#
# The output of one runnable automatically becomes the input to the next
# runnable, making it easy to build multi-step AI workflows.
#
# Example:
#
# User Input
#      ↓
# PromptTemplate
#      ↓
# LLM
#      ↓
# Output Parser
# =============================================================================
    
# LCEL (LangChain Expression Language) is a declarative way to build and connect AI components like prompts, models, and output parsers using the pipe operator (|). It makes code clean, modular, and ready for production.    
    
# =============================================================================
# Why don't we explicitly create a RunnableSequence?
#
# In LCEL, every component such as PromptTemplate, Chat Model, and
# Output Parser is already a Runnable.
#
# When we connect them using the "|" operator, LangChain automatically
# creates a RunnableSequence behind the scenes.
#
# So the following:
#
# prompt | llm | StrOutputParser()
#
# is actually equivalent to creating a RunnableSequence.
# =============================================================================    