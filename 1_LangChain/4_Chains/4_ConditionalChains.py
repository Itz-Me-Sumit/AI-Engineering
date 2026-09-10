from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel , RunnableBranch , RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel , Field
from typing import Optional , Literal
from dotenv import load_dotenv

load_dotenv()

class FeedbackOutput(BaseModel):
    sentiment : Optional[Literal["positive" , "negative"]] = Field(
        description = "give the sentiment of feedback in positive or negative"
    )

str_parser = StrOutputParser()
pydantic_parser = PydanticOutputParser(pydantic_object = FeedbackOutput)

model = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash"
)


sentiment_prompt = PromptTemplate(
    template = "Classify the sentiment of the following feedback text into positive or negative\n{feedback}\n{format_instructions}",
    input_variables = ["feedback"],
    partial_variables = {
        "format_instructions" : pydantic_parser.get_format_instructions()
    }
)

classifier_chain = sentiment_prompt | model | pydantic_parser

pos_sentiment_response_prompt = PromptTemplate(
    template = "write an appropriate response for this positive feedback\n feedback -> {feedback}",
    input_variables = ["feedback"]
)
neg_sentiment_response_prompt = PromptTemplate(
    template = "write an appropriate response for this negaitve feedback\n feedback -> {feedback}",
    input_variables = ["feedback"]
)

branch_chain = RunnableBranch(
    (lambda x : x.sentiment == "positive" , pos_sentiment_response_prompt | model | str_parser),
    (lambda x : x.sentiment == "negative" , neg_sentiment_response_prompt | model | str_parser),
    RunnableLambda(lambda x : "Could not find any sentiment")    
)

final_chain = classifier_chain | branch_chain

response = final_chain.invoke({
    "feedback" : "Damnn bruhh it is terrable phone !!"
})

print(response)

final_chain.get_graph().print_ascii()