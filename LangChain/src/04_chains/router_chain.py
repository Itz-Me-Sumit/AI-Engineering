from pathlib import Path
import sys

# Add the project root to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from pydantic import BaseModel, Field
from typing import Annotated, Literal

from llm_client import get_llm


# ============================================================
# Structured Output Model
# ============================================================

class OutputStr(BaseModel):

    query_type: Annotated[
        Literal["science", "coding", "general"],
        Field(
            description=(
                "Classify the query into exactly one category: "
                "science, coding, or general"
            )
        )
    ]


# ============================================================
# Main
# ============================================================

def main():

    # --------------------------------------------------------
    # 1. Get LLM
    # --------------------------------------------------------

    llm = get_llm()


    # --------------------------------------------------------
    # 2. Get User Input
    # --------------------------------------------------------

    user_input = input("User : ")


    # --------------------------------------------------------
    # 3. Classifier
    # --------------------------------------------------------

    classifier = llm.with_structured_output(OutputStr)

    classification = classifier.invoke(user_input)

    query_type = classification.query_type

    print("\nQuery Type :", query_type)


    # --------------------------------------------------------
    # 4. Science Chain
    # --------------------------------------------------------

    science_chain = (
        PromptTemplate.from_template(
            """
            Explain the following Science Concept in a simple
            and beginner-friendly way.

            Question:
            {query}
            """
        )
        | llm
        | StrOutputParser()
    )


    # --------------------------------------------------------
    # 5. Coding Chain
    # --------------------------------------------------------

    coding_chain = (
        PromptTemplate.from_template(
            """
            Explain the following Programming Question in a
            simple and beginner-friendly way.

            Question:
            {query}
            """
        )
        | llm
        | StrOutputParser()
    )


    # --------------------------------------------------------
    # 6. General Chain
    # --------------------------------------------------------

    general_chain = (
        PromptTemplate.from_template(
            """
            Explain the following question in a simple and
            beginner-friendly way.

            Question:
            {query}
            """
        )
        | llm
        | StrOutputParser()
    )


    # --------------------------------------------------------
    # 7. Router Function
    # --------------------------------------------------------

    def route(data):

        query_type = data["query_type"]
        query = data["query"]

        if query_type == "science":

            return science_chain.invoke({
                "query": query
            })

        elif query_type == "coding":

            return coding_chain.invoke({
                "query": query
            })

        else:

            return general_chain.invoke({
                "query": query
            })


    # --------------------------------------------------------
    # 8. Convert normal Python function
    #    into LangChain Runnable
    # --------------------------------------------------------

    router = RunnableLambda(route)


    # --------------------------------------------------------
    # 9. Invoke Router
    # --------------------------------------------------------

    response = router.invoke({

        "query_type": query_type,

        "query": user_input

    })


    # --------------------------------------------------------
    # 10. Final Response
    # --------------------------------------------------------

    print("\nAI :", response)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()