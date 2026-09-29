from langgraph.graph import StateGraph , START , END
from langgraph.graph.message import BaseMessage , add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode , tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import sqlite3
from langchain_openrouter import ChatOpenRouter
from typing import TypedDict , Annotated
import requests
from dotenv import load_dotenv
load_dotenv()


# LLMs
llm = ChatOpenRouter(
    model = "openrouter/free"
)

# Tools
search_tool = DuckDuckGoSearchRun(region = "us-en")


@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}




@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()


tools = [search_tool, get_stock_price, calculator]
llm_with_tools = llm.bind_tools(tools)


# State
class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]

# Nodes
def chat_node(state : ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {
        "messages" : [response]
    }

tool_node = ToolNode(tools)

# DataBase
conn = sqlite3.connect(
    database = "chatbot.db",
    check_same_thread = False
)

# Checkpointer
checkpointer = SqliteSaver(conn=conn)


graph = StateGraph(ChatState)

# Node
graph.add_node("chat_node" , chat_node)
graph.add_node("tools" , tool_node)

# Edges
graph.add_edge(START , "chat_node")
graph.add_conditional_edges("chat_node" , tools_condition)
graph.add_edge("tools" , "chat_node")


chatbot = graph.compile(checkpointer = checkpointer)



# Helper Functions

def retrive_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']["thread_id"])
    return list(all_threads)
