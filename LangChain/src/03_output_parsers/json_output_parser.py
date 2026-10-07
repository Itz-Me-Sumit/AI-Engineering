"""
File: json_output_parser.py

Description
-----------
Demonstrates how to generate and parse JSON responses using
LangChain's JsonOutputParser.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from llm_client import get_llm


def main() -> None:
    """Demonstrates JsonOutputParser."""

    llm = get_llm()

    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template="""
            Extract the following product information.

            - Product Name
            - RAM
            - Storage
            - Display Size
            - Price

            {format_instructions}

            Product Description:
            {product}
        """,
        input_variables=["product"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    prompt_value = prompt.invoke(
        {
            "product": (
                "The Apple MacBook Air M4 comes with 16GB RAM, "
                "512GB SSD storage, a 13.6-inch Liquid Retina display, "
                "and is priced at $1,199."
            )
        }
    )

    print("Formatted Prompt:\n")
    print(prompt_value.text)

    response = llm.invoke(prompt_value)

    print("Raw LLM Response:\n")
    print(response.content)

    parsed_response = parser.invoke(response)

    print("Parsed JSON:\n")
    print(parsed_response)

    print("Accessing Individual Fields:\n")

    for key, value in parsed_response.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()