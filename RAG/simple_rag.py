from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_google_genai import ChatGoogleGenerativeAI
import numpy as np

print("----- Simple Chat Bot -----")
print("type exit to quit\b")

model = ChatGoogleGenerativeAI(model = "gemini-3.6-flash")

# step 1 - Internal knowladge base
document = [
    "Company policy states that employees get 20 days of paid leave.",
    "Sumit is a Senior Data Scientist working in the AI team.",
    "The company follows a hybrid work model with 3 days in office.",
    "Employees receive health insurance and performance bonuses."
]

# step 2 - Create Embeddings
vectorizer = TfidfVectorizer()
doc_embeddings = vectorizer.fit_transform(document)

# step 3 - Retrival Function
def retrive(query , top_k=2):

    query_embeddings = vectorizer.transform([query])
    similarity = cosine_similarity(query_embeddings , doc_embeddings)[0]
    top_indicies = np.argsort(similarity)[::-1][:top_k]

    return [document[i] for i in top_indicies]

# step 4 - chat loop
while True:
    user_input = input("You : ")
    if user_input.lower() == "exit":
        break
    else:
        retrived_docs = retrive(user_input)
        context = "\n".join(retrived_docs)

        # step 5 - Augmented prompt
        message = [
            {
                "role" : "system",
                "content" : "Answer only using the provided context , if you does not found say , i don't know"
            },
            {
                "role" : "user",
                "content" : f"context : \n{context}\n\nquestion : \n{user_input}"
            }
        ]
        response = model.invoke(message)
        print(f"\nRetrived Context: \n")
        for doc in retrived_docs:
            print(f"-{doc}")
        print(f"\nbot's response : \n{response.content[0]['text']}\n")