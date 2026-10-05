import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel , Field
from typing import Literal , Annotated

class sentimentStructure(BaseModel):
    sentiment : Annotated[
        Literal[
            "billing" , "technical issue" , "account management",
            "feature request" , "general inquiry"
        ],
        Field(
            description="categorize customer support tickets in these 5 category"
        )
    ]

def main():

    llm = get_llm()

    structured_llm = llm.with_structured_output(sentimentStructure)

    chat_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an AI assistant that categorizes customer support tickets.

                Classify each ticket into exactly one category from the following:

                - billing
                - technical issue
                - account management
                - feature request
                - general inquiry

                Respond ONLY with the category name.
                """,
            ),

            (
                "human",
                """
                Example 1

                Ticket:
                I was charged twice for my monthly subscription.

                Category:
                Billing

                ----------------------------------------

                Example 2

                Ticket:
                I forgot my password and can't log into my account.

                Category:
                Account Management

                ----------------------------------------

                Example 3

                Ticket:
                The mobile app crashes every time I upload a photo.

                Category:
                Technical Issue

                ----------------------------------------

                Now classify this ticket:

                Ticket:
                {ticket}

                Category:
                """,
            ),
        ]
    )

    chain = chat_prompt_template | structured_llm

    response = chain.invoke({
        """
        It would be great if your platform could support 
        dark mode for the dashboard.
        """
    })

    return response.sentiment


if __name__ == "__main__":
    print(main())