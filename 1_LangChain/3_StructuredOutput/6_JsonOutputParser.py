from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model = ChatHuggingFace(llm = llm)

parser = JsonOutputParser()

# 1st prompt
template = PromptTemplate(
    template = "Give me name , age and city of a fictional person\n{format_instruction}",
    input_variables = [],
    partial_variables = {
        "format_instruction" : parser.get_format_instructions()
    }
)

prompt = template.format()

print("Prompt:" + prompt)

chain = template | model | parser

response = chain.invoke({})

print(response)