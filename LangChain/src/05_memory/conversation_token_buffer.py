import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from llm_client import get_llm
from langchain_classic.memory import ConversationTokenBufferMemory
from langchain_core.messages import HumanMessage

def main():
    llm = get_llm()
    memory = ConversationTokenBufferMemory(
        llm = llm,
        max_token_limit = 100,
        return_messages = True
    )


    while True:

        user_input = input("User : ")
        if user_input.lower() == "exit":
            break

        history = memory.load_memory_variables({})

        messages = history["history"]

        messages.append(
            HumanMessage(content = user_input)
        )

        response = llm.invoke(messages)

        print(f"AI : {response.content}")

        memory.save_context(
            {"input" : user_input},
            {"output" : response.content}
        )


if __name__ == "__main__":
    main()