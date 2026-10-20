import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))




from pydantic import BaseModel , Field
from langchain_core.tools import tool , StructuredTool

class CalculatorInput(BaseModel):
    """ Input Schema for calculator tool """

    a : float = Field(description = "First Number")
    b : float = Field(description = "Second Number")

    operation : str = Field(desctiption = "A Mathematical Operation like add , substract , multiply  or divide")


def calculate(a: float , b:float , operation:str) -> float:
    "It Performs a Mathematical operation on two numbers"

    if operation == "add":
        return a+b
    elif operation == "substract":
        return a-b
    elif operation == "multiply":
        return a*b
    elif operation == "divide":
        if b == 0 :
            raise ValueError("denominator can't be zero")
        return a/b
    else:
        return "Operation not supported"



def main():

    calculator_tool = StructuredTool.from_function(
        func = calculate,
        name = "caluclator",
        description = "perform mathematical opeation on two numbers",
        args_schema = CalculatorInput
    )

    print(f"Calculator Name : {calculator_tool.name}")
    
    print(f"Calculator Description : {calculator_tool.description}")
    
    print(f"Calculator Input Schema : {calculator_tool.args_schema.model_json_schema()}")

    result = calculator_tool.invoke(
        {
            "a" : 20,
            "b" : 10,
            "operation" : "divide"
        }
    )

    print(f"Result : {result}")


if __name__ == "__main__":
    main()