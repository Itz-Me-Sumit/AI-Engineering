from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser , PydanticOutputParser
from pydantic import BaseModel , Field
from typing import Optional
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv

load_dotenv()


model = ChatGoogleGenerativeAI(model = "gemini-3.6-flash")

parser = StrOutputParser()

joke_prompt = PromptTemplate(
    template = "Give me a joke on this {topic}",
    input_variables = ["topic"]
)

joke_explain_prompt = PromptTemplate(
    template = "Explain the given {joke}",
    input_variables = ["joke"]
)

chain = RunnableSequence(joke_prompt , model , parser , joke_explain_prompt , model , parser)

"""
chain = prompt | model | parser
"""

response = chain.invoke({
    "topic" : "resume"
})

print(response)