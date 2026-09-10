from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-3.6-flash")

parser = StrOutputParser()

prompt1 = PromptTemplate(
    template = "give me a proper report on {topic} in 100 words",
    input_variables = ["topic"]
)

prompt2 = PromptTemplate(
    template = "summarize {text} in 5 short points",
    input_variables = ["text"]
)

chain = prompt1 | model | parser | prompt2 | model | parser

res = chain.invoke({
    "topic" : "unemployment in india"
})

print(res)

chain.get_graph().print_ascii()