import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from llm_client import get_llm
from pydantic import BaseModel , Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.output_parsers import OutputFixingParser


class Employee(BaseModel):
    name: str = Field(description="Employee's full name")
    department: str = Field(description="Department name")
    experience: int = Field(description="Years of experience")
    skills: list[str] = Field(description="List of technical skills")

def main():
    llm = get_llm()

    parser = PydanticOutputParser(pydantic_object = Employee)

    fixing_parser = OutputFixingParser.from_llm(
        llm = llm,
        parser = parser
    )

    malformed_output = malformed_output = """
        "name": "Rahul Sharma",
        "department": "AI",
        "experience": "5 years",
        "skills": "Python, SQL, LangChain"
    """

    parsed_response = fixing_parser.invoke(malformed_output)

    print(parsed_response)


if __name__ == "__main__":
    main()