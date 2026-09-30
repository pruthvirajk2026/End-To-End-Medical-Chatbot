from flask import Flask, render_template, request
from src.helper import download_hugging_face_embeddings
from src.pinecone_utils import get_pinecone_index_name, initialize_pinecone
from langchain.vectorstores import Pinecone
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import prompt_template

app = Flask(__name__)

load_dotenv()

index_name = get_pinecone_index_name()
initialize_pinecone(index_name)

embeddings = download_hugging_face_embeddings()

#Loading the index
docsearch=Pinecone.from_existing_index(index_name, embeddings)


PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])

chain_type_kwargs={"prompt": PROMPT}

llm=CTransformers(model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                  model_type="llama",
                  config={'max_new_tokens':512,
                          'temperature':0.8})


qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)



@app.route("/")
def index():
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form.get("msg", "").strip()
    if not msg:
        return "Message cannot be empty.", 400

    result = qa({"query": msg})
    return str(result["result"])



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=False)
