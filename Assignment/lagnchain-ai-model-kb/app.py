# ==========================================================
# PDF KNOWLEDGE BASE AI ASSISTANT USING LANGCHAIN
# ==========================================================

# This project demonstrates:
#
# 1. PDF Loading
# 2. Text Splitting
# 3. Embeddings
# 4. Vector Database
# 5. Retrieval
# 6. Prompting
# 7. LLM Response Generation
#
# Architecture:
#
# PDF → Chunks → Embeddings → Vector DB
#                                  ↓
# User Question → Retriever → LLM → Answer
# ==========================================================


# ==========================================================
# STEP 1: LOAD ENVIRONMENT VARIABLES
# ==========================================================

from dotenv import load_dotenv

load_dotenv()


# ==========================================================
# STEP 2: IMPORT REQUIRED COMPONENTS
# ==========================================================

# PDF Loader
# Reads PDF documents
from langchain_community.document_loaders import PyPDFLoader


# Text Splitter
# Splits large text into smaller chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter


# OpenAI Embeddings
# Converts text into vector representations
from langchain_openai import OpenAIEmbeddings


# FAISS Vector Store
# Stores and searches vectors efficiently
from langchain_community.vectorstores import FAISS


# ChatOpenAI Model
# Main LLM used for answering questions
from langchain_openai import ChatOpenAI


# Prompt Template
# Creates structured prompts
from langchain_core.prompts import ChatPromptTemplate


# Output Parser
# Converts response into plain text
from langchain_core.output_parsers import StrOutputParser


# ==========================================================
# STEP 3: LOAD PDF DOCUMENT
# ==========================================================

# Load the PDF file
loader = PyPDFLoader("xuv700-sample.pdf")

# Extract text from PDF
documents = loader.load()

print(f"Loaded {len(documents)} pages from PDF")


# ==========================================================
# STEP 4: SPLIT DOCUMENT INTO CHUNKS
# ==========================================================

# Why splitting is needed:
#
# LLMs cannot process extremely large text at once.
#
# So we divide text into smaller overlapping chunks.

text_splitter = RecursiveCharacterTextSplitter(
    
    # Maximum size of each chunk
    chunk_size=1000,
    
    # Overlap between chunks
    # Helps preserve context
    chunk_overlap=200
)

# Create chunks
chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} text chunks")


# ==========================================================
# STEP 5: CREATE EMBEDDINGS
# ==========================================================

# Embeddings convert text into numerical vectors.
#
# Similar meaning → similar vectors.

embeddings = OpenAIEmbeddings()


# ==========================================================
# STEP 6: STORE EMBEDDINGS IN VECTOR DATABASE
# ==========================================================

# FAISS stores vectors locally.
#
# It allows semantic similarity search.

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

print("Vector database created successfully")


# ==========================================================
# STEP 7: CREATE RETRIEVER
# ==========================================================

# Retriever searches for relevant chunks
# based on user question.

retriever = vectorstore.as_retriever(

    # Number of chunks to retrieve
    search_kwargs={"k": 3}
)


# ==========================================================
# STEP 8: CREATE LLM
# ==========================================================

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# ==========================================================
# STEP 9: CREATE PROMPT TEMPLATE
# ==========================================================

prompt = ChatPromptTemplate.from_template(
    """
    You are an AI assistant.

    Answer the user's question ONLY using the provided context.

    Context:
    {context}

    Question:
    {question}

    If the answer is not in the context,
    say:
    "I could not find the answer in the document."
    """
)


# ==========================================================
# STEP 10: CREATE OUTPUT PARSER
# ==========================================================

output_parser = StrOutputParser()


# ==========================================================
# STEP 11: ASK USER QUESTION
# ==========================================================

question = input("Ask a question about the PDF: ")


# ==========================================================
# STEP 12: RETRIEVE RELEVANT CHUNKS
# ==========================================================

# Semantic search happens here

retrieved_docs = retriever.invoke(question)


# Combine retrieved chunks into one context string
context_text = "\n\n".join(
    doc.page_content for doc in retrieved_docs
)


# ==========================================================
# STEP 13: CREATE CHAIN
# ==========================================================

chain = prompt | llm | output_parser


# ==========================================================
# STEP 14: GENERATE RESPONSE
# ==========================================================

response = chain.invoke({
    "context": context_text,
    "question": question
})


# ==========================================================
# STEP 15: PRINT RESPONSE
# ==========================================================

print("\n================ ANSWER ================\n")
print(response)