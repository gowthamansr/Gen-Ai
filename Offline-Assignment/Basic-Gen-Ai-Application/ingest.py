import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

def build_vector_database():
    source_file_path = "data/travel_policy.txt"
    persist_directory = "./chroma_db"
    
    if not os.path.exists(source_file_path):
        print(f"❌ Error: Source document not found at {source_file_path}. Please create it first.")
        return

    print("📖 Loading custom travel knowledge source text...")
    loader = TextLoader(source_file_path, encoding="utf-8")
    raw_documents = loader.load()

    print("✂️ Chunking text down into searchable document blocks...")
    # Recursive text splitters prevent cutting sentences or concepts in half
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    split_docs = text_splitter.split_documents(raw_documents)

    print("🧠 Computing mathematical vector embeddings via OpenAI...")
    embedding_engine = OpenAIEmbeddings(model="text-embedding-3-small")

    print(f"💾 Saving data chunks natively to disk database at '{persist_directory}'...")
    Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_engine,
        persist_directory=persist_directory
    )
    print("✨ Vector storage ingestion complete! You can now close this pipeline.")

if __name__ == "__main__":
    build_vector_database()