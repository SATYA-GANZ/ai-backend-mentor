import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

print("loading indexing chromadb")

load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
  raise ValueError("API_KEY Environtment not been set, set it first at .env file")

print("load file")
loader = TextLoader("./digitalBase.txt", encoding="utf-8")
documents = loader.load()
print("doccuments succesfully set")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

chunks = text_splitter.split_documents(documents)

# embedding to vector database chromadb
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

# db dir
db_dir = "./db"

db = Chroma.from_documents(chunks, embeddings, persist_directory=db_dir)

print("success index chromadb")