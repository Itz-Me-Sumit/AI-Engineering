"""
File: messages_placeholder.py

Description
-----------
Demonstrates how to use MessagesPlaceholder in ChatPromptTemplate.

MessagesPlaceholder allows us to dynamically insert conversation history
into a prompt. This is commonly used when building conversational AI
applications and chatbots.
"""

from pathlib import Path
import sys

# -------------------------------------------------------------------
# Add the project root to Python's module search path.
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from llm_client import get_llm
from utils.helpers import print_separator, print_title


def main() -> None:
    """Demonstrates MessagesPlaceholder."""

    print_title("MessagesPlaceholder")

    llm = get_llm()

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI tutor who answers questions based on the ongoing conversation.",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )

    # Simulated conversation history
    chat_history = [
        HumanMessage(content="What is LangChain?"),
        AIMessage(
            content=(
                "LangChain is a framework for building applications "
                "powered by Large Language Models."
            )
        ),
        HumanMessage(content="What are Prompt Templates?"),
        AIMessage(
            content=(
                "Prompt Templates help create reusable prompts by "
                "allowing dynamic variables."
            )
        ),
    ]

    messages = chat_prompt.invoke(
        {
            "chat_history": chat_history,
            "question": "Can you summarize both concepts in simple terms?",
        }
    )

    print("Formatted Messages:\n")

    for message in messages.messages:
        print(f"{message.type.upper()}:")
        print(message.content)
        print()

    print_separator()

    response = llm.invoke(messages)

    print("LLM Response:\n")
    print(response.content)


if __name__ == "__main__":
    main()