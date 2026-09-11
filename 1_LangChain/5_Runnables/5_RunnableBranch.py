from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableBranch, RunnableLambda

load_dotenv()

report_prompt = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)

summary_prompt = PromptTemplate(
    template='Summarize the following text \n {text}',
    input_variables=['text']
)

model = ChatGoogleGenerativeAI(model = "gemini-3.6-flash")

parser = StrOutputParser()

report_gen_chain = report_prompt | model | parser

branch_chain = RunnableBranch(
    (lambda x: len(x.split())>300, summary_prompt | model | parser),
    RunnablePassthrough()
)

final_chain = RunnableSequence(report_gen_chain, branch_chain)

print(final_chain.invoke({'topic':'Russia vs Ukraine'}))


