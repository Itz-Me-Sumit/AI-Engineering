from langchain_huggingface import ChatHuggingFace , HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers.structured import StructuredOutputParser , ResponseSchema

llm = HuggingFaceEndpoint(
    repo_id = "google/gemma-2-2b-it",
    task = "text-generation"
)

model = ChatHuggingFace(llm = llm)

schema = [
    ResponseSchema(name="fact_1" , description = "Fact 1 about topic"),
    ResponseSchema(name="fact_2" , description = "Fact 2 about topic"),
    ResponseSchema(name="fact_3" , description = "Fact 3 about topic"),
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template = "Give 3 facts about{ topic} \n{format_instruction}",
    input_variables = ["topic"],
    partial_variables = {
        "format_instruction" : parser.get_format_instructions()
    }
)

prompt = template.invoke({
    "topic" : "black hole"
})

response = model.invoke(prompt)

final_result = parser.parse(response.content)

print(final_result)