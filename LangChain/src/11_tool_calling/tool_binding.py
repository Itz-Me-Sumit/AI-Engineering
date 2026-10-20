import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from llm_client import get_llm
from langchain_core.tools import tool

@tool
def multiply(a:float , b:float)->float:
    """multiply two numbers"""
    return a * b

@tool
def add(a:float , b:float)->float:
    """add two numbers"""
    return a+b

def main():
    llm = get_llm()

    tools = [multiply , add]

    tool_by_name = {tool.name : tool for tool in tools}

    llm_with_tools = llm.bind_tools(tools)


    messages = [
        {
            "role" : "user",
            "content" : "what are the multiplication and addition of 2 and 3"
        }
    ]

    response = llm_with_tools.invoke(messages)

    messages.append(response)


    for tool_call in response.tool_calls:
        selected_tool = tool_by_name[tool_call["name"]]
        result = selected_tool.invoke(tool_call["args"])

        messages.append({
            "role":"tool",
            "content" : str(result),
            "tool_call_id" : tool_call["id"]
        })

    final_response = llm_with_tools.invoke(messages)

    print(f"Result : {final_response.content}")
    

if __name__ == "__main__":
    main()