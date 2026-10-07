import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage , HumanMessage

def main():

    llm = get_llm()

    chat_history = InMemoryChatMessageHistory()

    prompt = ChatPromptTemplate(
        [

            (

                "system",
                """
                You're a helpfull AI assistent
                """

            ),

            MessagesPlaceholder(
                variable_name = "chat_history"
            ),

            (

                "human",
                "{user_input}"

            )

        ]
    )


    while True:
        
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        messages = prompt.format_messages(
            chat_history = chat_history.messages,
            user_input = user_input
        )


        response = llm.invoke(messages)

        print("AI:", response.content)

        chat_history.add_user_message(user_input)
        chat_history.add_ai_message(response.content)


if __name__ == "__main__":
    main()