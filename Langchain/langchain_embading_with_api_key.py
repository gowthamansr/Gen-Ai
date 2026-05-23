from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings

# Load .env file
load_dotenv()

openai_embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

text_embed = "This is one of the best Gen AI courses I have ever taken. I highly recommend it to anyone interested in learning about GenAI."

embedding = openai_embeddings.embed_query(text_embed)

print(embedding[:5])