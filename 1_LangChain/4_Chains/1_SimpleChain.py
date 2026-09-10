from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import PydanticOutputParser , JsonOutputParser
from typing import Optional
from pydantic import BaseModel , Field
from dotenv import load_dotenv

load_dotenv()


model = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash"
)

class OutputFormat(BaseModel):

    topic_info : Optional[str] = Field(
        description = "give breif info about topic"
    )
    facts_list : Optional[list[str]] = Field(
        description = "give a single list containig asked number of facts"
    )

    
# parser = PydanticOutputParser(pydantic_object = OutputFormat)
parser = JsonOutputParser()

template = PromptTemplate(
    template = "Generate 5 instresting facts about {topic}\n{format_instructions}",
    input_variables = ["topic"],
    partial_variables = {"format_instructions" : parser.get_format_instructions()}
)



chain = template | model | parser

response = chain.invoke({
    "topic" : "Cricket"
})

print(response + "\n\n")