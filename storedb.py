import mysql.connector
import os
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

folder = r"C:\Users\rohit\Downloads\coe_assignment\output"

# Splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)

# Load all PDF documents
all_docs = []
pdf_files = [f for f in os.listdir(folder) if f.endswith(".pdf")]

for file in pdf_files:
    file_path = os.path.join(folder, file)
    print(f"Loading {file}...")
    loader = PyPDFLoader(file_path)
    all_docs.extend(loader.load())

# Split documents into chunks
splits = text_splitter.split_documents(all_docs)
print(f"Number of chunks: {len(splits)}")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Password123@",
    database="coe_pdfs_1"
)
cursor = conn.cursor()


# Insert query without datetime
insert_query = """
INSERT INTO pdf_chunks 
(content, source, page_number, page_label, total_pages, producer, creator, keywords)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""


for doc in splits:
    meta = doc.metadata
    cursor.execute(insert_query, (
        doc.page_content,
        meta.get("source", "unknown"),
        meta.get("page", 0),
        meta.get("page_label", ""),
        meta.get("total_pages", 1),
        meta.get("producer", ""),
        meta.get("creator", ""),
        meta.get("keywords", "")
    ))

conn.commit()
cursor.close()
conn.close()
print("All chunks inserted")
