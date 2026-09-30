## Push my Vector to the vector DB

from src.helper import load_pdf, text_split, download_hugging_face_embeddings
from src.pinecone_utils import get_pinecone_index_name, initialize_pinecone
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv

load_dotenv()

index_name = get_pinecone_index_name()
initialize_pinecone(index_name)


extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)
embeddings = download_hugging_face_embeddings()


#Creating Embeddings for Each of The Text Chunks & storing
docsearch=Pinecone.from_texts([t.page_content for t in text_chunks], embeddings, index_name=index_name)