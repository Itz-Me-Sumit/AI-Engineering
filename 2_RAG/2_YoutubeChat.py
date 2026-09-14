from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel , RunnableLambda , RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# embedding_model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)
# Generative_model
generative_model = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash"
)


# Fetching Youtube Transcript
video_id = "Gfr50f6ZBvo" 
try:
    ytt_api = YouTubeTranscriptApi()

    transcript = ytt_api.fetch(
        video_id,
        languages=["en"]
    )

    transcript_text = " ".join(
        snippet.text for snippet in transcript
    )

except TranscriptsDisabled:
    print("No captions available for this video.")



# Text Splitting
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)
chunks = splitter.create_documents([transcript_text])


# Vector store
vector_store = FAISS.from_documents(
    documents = chunks,
    embedding = embedding_model
)

# Retriever
retriever = vector_store.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k" : 4}
)

def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text


prompt = PromptTemplate(

    template = """
    you are a helpful assistent.
    Asnwer ONLY from provided transcript context.
    If context is insufficient , just say you don't know

    {context}
    question : {question}

    """,

    input_variables = ["context" , "question"]
    
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
   "context" : retriever | RunnableLambda(format_docs),
   "question" : RunnablePassthrough()
})

main_chain = parallel_chain | prompt | generative_model | parser

result = main_chain.invoke(
   "can you summarize the video"
)


print(f"Result : \n{result}")