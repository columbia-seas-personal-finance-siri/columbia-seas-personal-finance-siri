import functions_framework
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_experimental.chat_models import Llama2Chat
from langchain.llms import HuggingFaceTextGenInference
from langchain.prompts import PromptTemplate

template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.
AI will give the related information to answer: {color}

answer:"""
prompt = PromptTemplate.from_template(template)

llm = HuggingFaceTextGenInference(
  inference_server_url="http://localhost:8010/",
  max_new_tokens=512,
  top_k=50,
  temperature=0.1,
  repetition_penalty=1.03,
)

model = Llama2Chat(llm=llm)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = LLMChain(
  llm=model, 
  prompt=prompt,
  memory=memory)

@functions_framework.http
def llama_hf_call(request):  
  request_json = request.get_json(silent=True)
  request_args = request.args

  question = (request_json or request_args).get('question', 'Hi')
  answer = chain.invoke({"color" : question})

  return answer


