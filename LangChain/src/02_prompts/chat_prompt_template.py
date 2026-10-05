from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from langchain_core.prompts import ChatPromptTemplate
from llm_client import get_llm

def main():

    llm = get_llm()

    chat_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system" , 
                "You are a GenAI Teacher , who explains concepts in simple language"
            ),

            (
                "human" , 
                "{question}"
            ),

        ],
    )

    chain = chat_prompt_template | llm

    response = chain.invoke({
        "question":"What is RAG",
    })

    print(response.content)


if __name__ == "__main__":
    main()