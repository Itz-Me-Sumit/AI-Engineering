from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model = ChatHuggingFace(llm = llm)

# 1st prompt
template1 = PromptTemplate(
    template = "write a detailed report on {topic}",
    input_variables = ["topic"]
)

# 2nd prompt
template2 = PromptTemplate(
    template = "write a 5 line summary on the following text\n{text}",
    input_variables = ["text"]
)

"""
prompt1 = template1.invoke( 
    {
        "topic" : "black hole"
    }
)
prompt1_response = model.invoke(prompt1)


prompt2 = template2.invoke(
    {
        "text" : prompt1_response.content
    }
)
prompt2_response = model.invoke(prompt2)
"""

parser = StrOutputParser()
chain = template1 | model | parser | template2 | model | parser


response = chain.invoke(
    {
        "topic" : "Black Hole"
    }
)

print(response)