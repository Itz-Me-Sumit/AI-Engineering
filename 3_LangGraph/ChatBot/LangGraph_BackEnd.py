from langgraph.graph import StateGraph , START , END
from langgraph.graph.message import BaseMessage , add_messages
from langgraph.checkpoint.memory import InMemorySaver
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
        "messages" : response.content
    }



graph = StateGraph(ChatState)

# Node
graph.add_node("chat_node" , chat_node)


# Edges
graph.add_edge(START , "chat_node")
graph.add_edge("chat_node" , END)


checkpointer = InMemorySaver()

graph.compile()

