"""
File: model_parameters.py

Description
-----------
Demonstrates the commonly used LLM parameters and how they influence
the model's behavior.

Parameters Covered:
- Temperature
- Max Tokens
- Top-P
- Frequency Penalty
- Presence Penalty
- Stop Sequences
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from llm_client import get_llm


# -------------------------------------------------------------------
# Parameter demonstrations
# -------------------------------------------------------------------
PARAMETER_DEMOS = [
    {
        "title": "Temperature",
        "description": (
            "Controls randomness. Lower values generate more deterministic "
            "responses, while higher values generate more creative responses."
        ),
        "params": {"temperature": 0.1},
        "prompt": "Suggest three AI startup ideas.",
    },
    {
        "title": "Max Tokens",
        "description": (
            "Limits the maximum number of tokens the model can generate."
        ),
        "params": {"max_tokens": 50},
        "prompt": "Explain LangChain in detail.",
    },
    {
        "title": "Top-P",
        "description": (
            "Controls nucleus sampling by selecting tokens from the most "
            "probable candidates."
        ),
        "params": {"top_p": 0.5},
        "prompt": "Suggest three AI startup ideas.",
    },
    {
        "title": "Frequency Penalty",
        "description": (
            "Reduces repetition by discouraging the model from using the "
            "same words repeatedly."
        ),
        "params": {"frequency_penalty": 1.2},
        "prompt": "Write a short paragraph about Artificial Intelligence.",
    },
    {
        "title": "Presence Penalty",
        "description": (
            "Encourages the model to introduce new ideas and vocabulary."
        ),
        "params": {"presence_penalty": 1.2},
        "prompt": "Suggest future technologies for smart cities.",
    },
    {
        "title": "Stop Sequences",
        "description": (
            "Stops text generation when a specified sequence is encountered."
        ),
        "params": {"stop": ["4."]},
        "prompt": "List five popular programming languages as a numbered list.",
    },
]


def main() -> None:
    """
    Demonstrates commonly used LLM parameters.
    """

    llm = get_llm()

    for demo in PARAMETER_DEMOS:

        print(f"\n{demo['title']}")
        print("-" * len(demo["title"]))
        print(demo["description"])

        response = llm.bind(**demo["params"]).invoke(demo["prompt"])

        print("\nResponse:\n")
        print(response.content)


if __name__ == "__main__":
    main()