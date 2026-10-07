import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from llm_client import get_llm
from langchain_classic.memory import ConversationBufferMemory


def main():

    llm = get_llm()

    memory = ConversationBufferMemory(return_messages = True)

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        # Previous conversation + current input
        history = memory.load_memory_variables({})
        messages = history["history"]

        messages.append(
            ('human' , user_input)
        )

        response = llm.invoke(messages)

        print("AI :" , response.content)

        # Saving current conversation into memory
        memory.save_context(
            {"input" : user_input,},
            {"output" : response.content}
        )


if __name__ == "__main__":
    main()