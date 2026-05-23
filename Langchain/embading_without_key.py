from langchain_community.embeddings import HuggingFaceEmbeddings
hugging_face_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

text_embed = "This is one of the best Gen AI courses I have ever taken. I highly recommend it to anyone interested in learning about GenAI."
hugging_face_embedd = hugging_face_embeddings.embed_query(text_embed)
print(hugging_face_embedd[:5])