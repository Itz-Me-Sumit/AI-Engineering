from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Optional
from pydantic import BaseModel , Field 
from dotenv import load_dotenv


load_dotenv()

model = HuggingFaceEndpoint(
    repo_id = "google/gemma-2-2b-it",
    task = "text-generation"
)

class Person(BaseModel):

    name : Optional[str] = Field(
        description = "Name of the person"
    )
    age : Optional[int] = Field(
        ge = 18 , le = 130,
        description = "Age of person"
    )
    city : Optional[str] = Field(
        description = "City where person lives or belongs to"
    )
    
parser = PydanticOutputParser(pydantic_object = Person)

template = PromptTemplate(
    template = "Generate Age , Name and City of a fictional {place} person \n{format_instructions}",
    input_variables = ["place"],
    partial_variables = {"format_instructions" : parser.get_format_instructions()}
)

chain = template | model | parser

response = chain.invoke({
    "place" : "India"
})

print(response)