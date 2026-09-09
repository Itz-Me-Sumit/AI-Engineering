# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict , Annotated , Optional , Literal

load_dotenv()

model = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
)

class Review(TypedDict):
    key_themes : Annotated[
        list[str], 
        "Write down all the key themes discussed in the review in a list"
    ]
    summary : Annotated[
        str, 
        "A brief summary of the review"
    ]
    sentiments : Annotated[
        str, 
        "Return sentiment of review either negative , positive ,neutral"
    ]
    sentiment : Annotated[
        Literal["Positive" , "Negative"],
        "Return sentiment of review either negative , positive ,neutral"
    ]

    pros : Annotated[
        Optional[list[str]],
        "Write down all the pros in the list"
    ]
    cons : Annotated[
        Optional[list[str]],
        "Write down all the cons in the list"
    ]

structured_model = model.with_structured_output(Review)


res = structured_model.invoke("""

I recently upgraded to the Samsung Galaxy S24 Ultra, and I must say, it's an absolute powerhouse! The Snapdragon 8 Gen 3 processor makes everything lightning fast—whether I'm gaming, multitasking, or editing photos. The 5000mAh battery easily lasts a full day even with heavy use, and the 45W fast charging is a lifesaver.

The S-Pen integration is a great touch for note-taking and quick sketches, though I don't use it often. What really blew me away is the 200MP camera—the night mode is stunning, capturing crisp, vibrant images even in low light. Zooming up to 100x actually works well for distant objects, but anything beyond 30x loses quality.

However, the weight and size make it a bit uncomfortable for one-handed use. Also, Samsung's One UI still comes with bloatware—why do I need five different Samsung apps for things Google already provides? The $1,300 price tag is also a hard pill to swallow.

Pros:
Insanely powerful processor (great for gaming and productivity)
Stunning 200MP camera with incredible zoom capabilities
Long battery life with fast charging
S-Pen support is unique and useful
                                 
Review by Nitish Singh

""")

print(res)
print()

print(f"Key Themes : {res['key_themes']}")
print()

print("Summary : " + res["summary"])
print()

print("Semtiments : " , res["sentiments"])
print()

print("Semtiment : " , res["sentiment"])
print()

print(f"Pros : {res['pros']}")
print()

print(f"Cons : {res['cons']}")
print()