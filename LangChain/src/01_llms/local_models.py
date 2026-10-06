import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

def main():

    "Local LLM using Ollama"

    llm = ChatOllama(
        model = "mistral",
        temperature = 0.7,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system" , "you're a really good chef how know to cook {food_type}"),
            ("human" , "please give me recipe of {food}")
        ]
    )

    chain = prompt | llm 

    response = chain.invoke({
        "food_type" : "non-vegaterian",
        "food" : "Mutton"
    })

    print(response.content)


if __name__ == "__main__":
    main()