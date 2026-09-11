from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel , RunnableSequence
from dotenv import load_dotenv

load_dotenv()

tweet_prompt = PromptTemplate(
    template = "Generate a tweet on {tweet_topic}",
    input_variables = ["tweet_topic"]
)

linkdinPost_prompt = PromptTemplate(
    template = "Generate a linkdin post about {linkdin_topic}",
    input_variables = ["linkdin_topic"]
)


gemini_model = ChatGoogleGenerativeAI(model = "gemini-3.6-flash")
groq_model = ChatGroq(model = "qwen/qwen3.6-27b", max_tokens = 500)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    "tweet" : RunnableSequence(tweet_prompt , gemini_model , parser),
    "linkdinPost" : RunnableSequence(linkdinPost_prompt , groq_model , parser)
})

# merge_chain = RunnableSequence(prompt3 , gemini_model , parser)

# final_chain = RunnableSequence(parallel_chain | merge_chain)

response  = parallel_chain.invoke({
    "tweet_topic" : "Artificial Intelligence",
    "linkdin_topic" : "Generative AI"
})

print(response)

parallel_chain.get_graph().print_ascii()