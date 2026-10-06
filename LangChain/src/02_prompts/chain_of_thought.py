import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from llm_client import get_llm
from langchain_core.prompts import ChatPromptTemplate

def main():

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages(
        [

            (
                "system",

                """
                You are an experienced insurance claims analyst.

                Think through the problem step by step before reaching your conclusion.
                Finally, provide:
                1. Your reasoning
                2. Your final decision
                """
            ),

            (
                "human",

                """
                A vehicle was insured on January 1.

                The policy covers accidents occurring after the policy start date.

                The customer reports:
                - Accident Date: January 15
                - Claim Filed: January 18
                - Premium Status: Paid
                - Police Report: Available
                - Estimated Repair Cost: $4,800

                Should this claim be approved? Explain your reasoning step by step.
                """
            )

        ]
    )

    chain = prompt | llm

    response = chain.invoke({})

    print(response.content)


if __name__ == "__main__":
    main()