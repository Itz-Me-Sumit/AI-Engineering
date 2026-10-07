"""
File: csv_output_parser.py

Description
-----------
Demonstrates how to generate structured tabular data in CSV format
using LangChain's CommaSeparatedListOutputParser.

Although the parser returns a list, the output can easily be converted
into CSV rows for reporting or downstream processing.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate

from llm_client import get_llm

def main() -> None:
    """Demonstrates CSV-style output parsing."""

    llm = get_llm()

    parser = CommaSeparatedListOutputParser()

    prompt = PromptTemplate(
        template="""
            List the top 10 programming languages used in AI development.

            {format_instructions}
        """,
        input_variables=[],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    prompt_value = prompt.invoke({})

    print("Formatted Prompt:\n")
    print(prompt_value.text)

    response = llm.invoke(prompt_value)

    print("Raw LLM Response:\n")
    print(response.content)

    languages = parser.invoke(response)

    print("Parsed Output:\n")

    print("Rank,Language")

    for index, language in enumerate(languages, start=1):
        print(f"{index},{language}")


if __name__ == "__main__":
    main()