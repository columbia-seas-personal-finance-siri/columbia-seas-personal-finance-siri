import functions_framework
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate



template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
AI will give the related information to answer: {color}

answer:"""
prompt = PromptTemplate.from_template(template)

llm = VertexAI(
    model_name="text-bison@001",
    max_output_tokens=256,
    temperature=0.1,
    top_p=0.8,
    top_k=40,
    verbose=True,
)

chain = prompt | llm
@functions_framework.http
def chat(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    question = (request_json or request_args).get('question', 'Hi')
    answer = chain.invoke({"color" : question})

    return answer
