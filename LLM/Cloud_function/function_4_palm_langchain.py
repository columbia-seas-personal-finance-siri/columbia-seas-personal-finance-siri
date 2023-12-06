import functions_framework
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate
from langchain.document_loaders import DirectoryLoader, TextLoader, GCSFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
def load_file(file_path):
    return TextLoader(file_path)
loader = GCSFileLoader(
    project_name="finsnap", bucket="finsnap-867a9.appspot.com", blob="qqz_table_Bankrate.json", loader_func=load_file
)
data = loader.load()
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs=text_splitter.split_documents(data)
embeddings=HuggingFaceEmbeddings()
vectorstore=FAISS.from_documents(docs, embeddings)
template = """my current template: A chat between a user and an artificial intelligence assistant, Finsnap. 
This AI assistant is a helpful, respectful and honest personal finance assistant. Its name is Finsnap. It is aimed to help user optimize expenditures, consolidate personalized offers and provide personal finance advice.
The assistant gives helpful, detailed, and polite answers to the user's questions. The answer from this assistant follow the follwoing rule:
  - Always prioritize the question over the chat history.
  - Ignore any chat history that is not directly related to the question.
  - Only attempt to answer if a question was posed.
  - The question should be within 3 sentences.
  - You should remove all emojis in the answer.
  - You should remove any words that are not relevant to the question.
  - If you are unable to formulate a question, respond with "Sorry, I don't know.".
  - If you need more information, ask user follow-up questions.
  - Response of AI is safe, without any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.
  - Please ensure that responses are socially unbiased and positive in nature.
  - write content like human talk, do not use over passive voice, do not use jargons, do not words like - overall, furthermore, in conclusions, that excessively.
AI will give the related information to the question.
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
memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True)
mem_qa=ConversationalRetrievalChain.from_llm(llm=llm,
                                             retriever=vectorstore.as_retriever(),
                                             memory=memory,
                                             get_chat_history=lambda h : h,
                                             prompt=prompt)
chain = prompt | llm
@functions_framework.http
def chat(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    question = (request_json or request_args).get('question', 'Hi')
    # answer = chain.invoke({"color" : question})
    result = mem_qa(question)
    answer = result['answer']
    return answer
