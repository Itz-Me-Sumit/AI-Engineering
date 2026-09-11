from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence , RunnableParallel , RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()


joke_prompt = PromptTemplate(
    template = "Tell me a joke about {topic}",
    input_variables = ["topic"]
)
joke_explain_prompt = PromptTemplate(
    template = "explain the joke {joke}",
    input_variables = ["joke"]
)

gemini_model = ChatGoogleGenerativeAI(model = "gemini-3.6-flash")
groq_model = ChatGroq(model = "qwen/qwen3.6-27b", max_tokens = 500)


parser = StrOutputParser()

joke_gen_chain = RunnableSequence(joke_prompt , gemini_model , parser)

parallel_chain = RunnableParallel({
    "joke" : RunnablePassthrough(),
    "explaination" : RunnableSequence(joke_explain_prompt , gemini_model , parser)
})

final_chain = RunnableSequence(joke_gen_chain , parallel_chain)

response = final_chain.invoke({
    "topic" : "cricket"
})

print(f"""

Joke : {response["joke"]}



Explaination : {response["explaination"]}

""")

final_chain.get_graph().print_ascii()