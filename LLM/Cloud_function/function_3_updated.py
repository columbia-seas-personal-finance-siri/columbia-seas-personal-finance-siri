import functions_framework
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
# loader
loader = JSONLoader(
    file_path='data.json',
    jq_schema='.messages[].content',
    text_content=False)

data = loader.load()
text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
docs=text_splitter.split_documents(data)
embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
vectorstore=FAISS.from_documents(docs, embeddings)

template = """Query the related information about the question: {color}

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

chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
# chain=prompt | ConversationalRetrievalChain.from_llm(llm=llm, retriever=vectorstore.as_retriever(), memory=memory,get_chat_history = lambda h:h)
@functions_framework.http
def chat(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    question = (request_json or request_args).get('question', 'Hi')
    answer = chain.invoke({"color" : question})

    return answer
