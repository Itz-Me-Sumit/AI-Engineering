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
        Literal["positive" , "negative"],
        Field(
            description="sentiment must be in either positive or negative"
        )
    ]

def main():

    llm = get_llm()

    structured_llm = llm.with_structured_output(sentimentStructure)

    chat_prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you're a expert sentiment analyst assistent"
            ),
            (
                "human",
                """
                    Classify the sentiment as Positive, Negative, or Neutral.

                    Example:

                    Review: "The laptop is fast, lightweight, and has an amazing battery life."
                    Sentiment: Positive
                    I
                    Now classify the following review:

                    Review: "{review}"

                """
            )
        ]
    )

    chain = chat_prompt_template | structured_llm

    response = chain.invoke({
        "dammnn i didn't expect that this Washing Maching will be that good"
    })

    return response.sentiment


if __name__ == "__main__":
    print(main())