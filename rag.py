# rag.py

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# 📁 Local path where FAISS index will be saved
VECTORSTORE_DIR = "vectorstore"

# 📂 Load all PDFs from structured folders
def load_all_pdfs(base_path="data"):
    all_docs = []
    subfolders = ["book", "lecture_slides", "mcqs", "resources"]
    
    for subfolder in subfolders:
        folder_path = os.path.join(base_path, subfolder)
        if not os.path.exists(folder_path):
            print(f"⚠️ Skipping missing folder: {folder_path}")
            continue

        for file in os.listdir(folder_path):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(folder_path, file)
                try:
                    loader = PyMuPDFLoader(pdf_path)
                    all_docs.extend(loader.load())
                    print(f"✅ Loaded: {pdf_path}")
                except Exception as e:
                    print(f"❌ Failed to load {pdf_path}: {e}")
    return all_docs

# ✂️ Split into chunks for embedding
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)

# 🤖 Embed and create FAISS vectorstore
def embed_and_save(chunks):
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedder)
    vectorstore.save_local(VECTORSTORE_DIR)
    print("💾 Vectorstore created and saved.")
    return vectorstore

# 📦 Load vectorstore (or create if not found)
def create_or_load_vectorstore():
    if os.path.exists(VECTORSTORE_DIR):
        print("📂 Loading existing vectorstore...")
        embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        return FAISS.load_local(VECTORSTORE_DIR, embedder, allow_dangerous_deserialization=True)
    else:
        print("🧠 Creating new vectorstore from PDFs...")
        raw_docs = load_all_pdfs()
        chunks = chunk_documents(raw_docs)
        return embed_and_save(chunks)

# 🧪 Run from terminal to build vectorstore
if __name__ == "__main__":
    create_or_load_vectorstore()
