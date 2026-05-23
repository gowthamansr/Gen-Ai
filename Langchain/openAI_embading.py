from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Load PDF
loader = PyPDFLoader("sample-1.pdf")
documents = loader.load()

# Split text
splitter = CharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = splitter.split_documents(documents)

# Embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# Vector store
vectorstore = FAISS.from_documents(
    docs,
    embeddings
)

# Query
results = vectorstore.similarity_search(
    "Summarize the document"
)

print(results[0].page_content)