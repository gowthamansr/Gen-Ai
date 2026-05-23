from dotenv import load_dotenv

load_dotenv()

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Sample texts
texts = [
    "LangChain helps build LLM applications.",
    "Chroma is a vector database.",
    "Hugging Face provides transformer models."
]

# HuggingFace embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create Chroma vector DB
vectorstore = Chroma.from_texts(
    texts=texts,
    embedding=embeddings,
    persist_directory="./chroma_hf_db"
)

# Similarity search
results = vectorstore.similarity_search(
    "What is Chroma?"
)

print(results[0].page_content)