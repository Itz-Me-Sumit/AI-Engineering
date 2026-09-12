from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

text = """

Every night, something remarkable happens inside our bodies: we enter a temporary world where our brain becomes highly active while our muscles become mostly still. Sleep may look like a period of complete rest, but the brain uses this time to perform several important tasks.

During sleep, the brain processes information collected throughout the day. Memories are organized, unnecessary information may be discarded, and important experiences are strengthened. This is one reason why getting enough sleep can improve learning and problem-solving. Students who study for hours but sleep very little may actually remember less than students who study for a shorter time and sleep properly.

Sleep also affects our emotions. After a good night's sleep, people often feel more patient, focused, and positive. In contrast, sleep deprivation can make small problems feel much bigger and can reduce our ability to make good decisions.

Scientists have discovered that sleep happens in different stages, including deep sleep and REM sleep. During REM sleep, our eyes move rapidly and vivid dreams are common. Interestingly, the brain can be almost as active during REM sleep as it is when we are awake.

So, sleep is not simply “doing nothing.” It is more like the brain's nightly maintenance session.


"""

# Simple Text splitter
text_splitter = CharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0,
    separator = ''
)

result = text_splitter.split_text(text)

for i , chunk in enumerate(result):
    print(f"Chunk {i} : \n{chunk}\n\n")



# Text spliter With PDF loader
pdf_loader = PyPDFLoader("Adventure.pdf")
docs = pdf_loader.load()

docs_text_splitter = CharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0,
    separator = ''
)
docs_text = docs_text_splitter.split_text(docs[0].page_content)

for i , chunk in enumerate(docs_text):
    print(f"Chunk : {i}\n{chunk}\n\n")



# use of split_documents in textsplitter
pdf_loader = PyPDFLoader("Adventure.pdf")
docs = pdf_loader.load()

docs_text_splitter = CharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0,
    separator = ''
)
docs_text = docs_text_splitter.split_documents(docs)

for i , chunk in enumerate(docs_text):
    print(f"Chunk : {i}\n{chunk.page_content}\n\n")