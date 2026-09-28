from langgraph.graph import StateGraph , START , END
from langgraph.graph.message import BaseMessage , add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langchain_openrouter import ChatOpenRouter
from typing import TypedDict , Annotated
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenRouter(
    model = "openrouter/free"
)

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]


def chat_node(state : ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {
        "messages" : [response]
    }


# DataBase
conn = sqlite3.connect(
    database = "chatbot.db",
    check_same_thread = False
)
checkpointer = SqliteSaver(conn=conn)

def retrive_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']["thread_id"])
    return list(all_threads)


graph = StateGraph(ChatState)

# Node
graph.add_node("chat_node" , chat_node)


# Edges
graph.add_edge(START , "chat_node")
graph.add_edge("chat_node" , END)


chatbot = graph.compile(checkpointer = checkpointer)