from langchain_core.messages import SystemMessage , HumanMessage , AIMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    temperature = 0.8,
)

messages = [
    SystemMessage(content = "You are a helpful assistent"),
    HumanMessage(content = "Tell me about LangChain")
]

res = model.invoke(messages)

messages.append(
    AIMessage(res.content)
)

print(messages)