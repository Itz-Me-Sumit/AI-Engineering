from pathlib import Path
import sys

# Adding the project root to Python's search path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from langchain_core.prompts import PromptTemplate
from llm_client import get_llm

def main():
    llm = get_llm()
    prompt_template = PromptTemplate(
        template="""
            You are the expert of {profession},
            Explain the concept {topic} in simple words,
            keep the explaination under {words} words
        """,
        input_variables= ["profession" , "topic" , "words"],
    )
    chain = prompt_template | llm
    response = chain.invoke({
        "profession" : "Data Scientist",
        "topic" : "Singular Value Decomposition",
        "words" : 200
    })
    return response.content

if __name__ == "__main__":
    print(main())