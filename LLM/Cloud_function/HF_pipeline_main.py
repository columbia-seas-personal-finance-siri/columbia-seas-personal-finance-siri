import functions_framework
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

model="meta-llama/Llama-2-7b-chat-hf"
tokenizer=AutoTokenizer.from_pretrained(model)
pipeline=transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    max_length=1000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id
    )

llm=HuggingFacePipeline(pipeline=pipeline, model_kwargs={'temperature':0.7})
template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
AI will give the related information to answer: {color}

answer:"""
prompt = PromptTemplate.from_template(template)
chain = ConversationChain(llm=llm, prompt=prompt)

@functions_framework.http
def llama_http(request):
  request_json = request.get_json(silent=True)
  request_args = request.args

  question = (request_json or request_args).get('question', 'Hi')
  answer = chain.invoke({"color" : question})

  return answer
