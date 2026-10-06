import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate


def chat_with_model() -> None :
    """
    Sends a simple prompt to the configured chat model and prints the response.
    This example demonstrates the most basic interaction with a LangChain chat model.
    """

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system" , "you're a professor of {profession}"),
        ("human" , "Explain me about {topic}")
    ])

    chain = prompt | llm 

    response = chain.invoke({
        "profession" : "Data Science",
        "topic" : "Poisson Distrubution"
    })

    print(response.content)



if __name__ == "__main__":
    chat_with_model()