from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
import os

print("Loading Model...")
model = HuggingFaceEmbeddings(model_name="FacebookAI/xlm-roberta-base")
folder = r"C:\Users\rohit\Downloads\coe_assignment\output"
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)

all_docs = []
pdf_files = [f for f in os.listdir(folder)]

# pdf_files = ["200303_Minutes-54-BoG.pdf", "180208_Minutes-48-BoG.pdf"]
for file in pdf_files:
    file_path = os.path.join(folder, file)
    print(f"Loading {file}...")
    loader = PyPDFLoader(file_path)
    all_docs.extend(loader.load())

print("Creating Splits...")
splits = text_splitter.split_documents(all_docs)
print(f"Number of chunks: {len(splits)}")
      
print("Creating Vectorstore...")
try:
    vectorstore = FAISS.from_documents(splits, model)
    print("Saving Vectorstore...")     
    vectorstore.save_local("faiss_index")
    print("Vectorstore saved successfully.")
except Exception as e:
    print("Error occurred while creating or saving vectorstore:", e)

