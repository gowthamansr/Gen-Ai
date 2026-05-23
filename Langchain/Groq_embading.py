from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

# -----------------------------
# GROQ LLM Don't have API-Key
# -----------------------------
llm = ChatGroq(
    groq_api_key="YOUR_GROQ_API_KEY",
    model_name="llama-3.3-70b-versatile"
)

# -----------------------------
# EMBEDDING MODEL
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# SAMPLE TEXT
# -----------------------------
text = """
LangChain helps developers build LLM applications.
Groq provides ultra-fast inference for open-source models.
"""

# -----------------------------
# SPLIT TEXT
# -----------------------------
splitter = CharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(text)

documents = [Document(page_content=chunk) for chunk in chunks]

# -----------------------------
# CREATE VECTOR STORE
# -----------------------------
vectorstore = FAISS.from_documents(
    documents,
    embeddings
)

# -----------------------------
# SIMILARITY SEARCH
# -----------------------------
results = vectorstore.similarity_search(
    "What does Groq provide?"
)

print(results[0].page_content)

# -----------------------------
# ASK GROQ
# -----------------------------
response = llm.invoke(
    "Explain Groq in one sentence."
)

print(response.content)