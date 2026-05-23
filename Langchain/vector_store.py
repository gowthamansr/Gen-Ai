from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

text = ["Python is a popular programming language.", "LangChain is a framework for building applications with LLMs.",
"This is one of the best Gen AI courses I have ever taken. I highly recommend it to anyone interested in learning about GenAI.",
"This course provides a comprehensive introduction to Gen AI concepts and techniques."]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.from_texts(text, embeddings)

vectorstore.save_local("my_vectorstoredb")