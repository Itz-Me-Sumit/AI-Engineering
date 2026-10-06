"""
File: partial_prompt.py

Description
-----------
Demonstrates Partial Prompt Templates.

A Partial PromptTemplate allows us to pre-fill one or more variables while
keeping the remaining variables dynamic. This is useful when certain parts
of a prompt remain constant across multiple LLM calls.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.prompts import PromptTemplate

from llm_client import get_llm


def main() -> None:
    """Demonstrates Partial PromptTemplate."""


    llm = get_llm()

    prompt_template = PromptTemplate(
        template="""
You are an expert {domain} trainer.

Explain the concept of {topic}.

Keep the explanation under {word_limit} words.
""",
        input_variables=["domain", "topic", "word_limit"],
    )

    # Pre-fill the domain once.
    partial_prompt = prompt_template.partial(domain="Generative AI")

    # Only the remaining variables are required.
    prompt = partial_prompt.invoke(
        {
            "topic": "Vector Embeddings",
            "word_limit": 100,
        }
    )

    print("Formatted Prompt:\n")
    print(prompt.text)

    response = llm.invoke(prompt)

    print("LLM Response:\n")
    print(response.content)


if __name__ == "__main__":
    main()