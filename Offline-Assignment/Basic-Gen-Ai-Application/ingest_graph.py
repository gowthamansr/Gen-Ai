# ingest_graph.py
import os
import networkx as nx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

# Setup an extraction engine to identify triplets (Subject, Relation, Object)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

extraction_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an advanced Knowledge Graph extraction engine.\n"
        "Read the text provided and extract explicit entities and relationships as atomic triplets.\n"
        "Return the output strictly as a JSON object containing a list under the key 'triplets'.\n"
        "Format: {{\"triplets\": [ {{\"subject\": \"Paris\", \"relation\": \"CLOSED_ON\", \"object\": \"Tuesday\"}} ]}}"
    )),
    ("user", "Extract triplets from this text:\n\n{text}")
])

extraction_chain = extraction_prompt | llm | JsonOutputParser()

def build_knowledge_graph():
    G = nx.DiGraph()
    
    # Read our travel rule source document 
    with open("./data/travel_policy.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Segment into operational sentences or short rule blocks
    chunks = [c.strip() for c in content.split("\n") if len(c.strip()) > 10]
    
    print(f"Parsing {len(chunks)} structural rule components into graph nodes...")
    
    for chunk in chunks:
        try:
            result = extraction_chain.invoke({"text": chunk})
            for triplet in result.get("triplets", []):
                sub = triplet["subject"].strip()
                obj = triplet["object"].strip()
                rel = triplet["relation"].strip()
                
                # Formulate graph architecture nodes and directional edges
                G.add_node(sub, type="Entity")
                G.add_node(obj, type="Entity")
                G.add_edge(sub, obj, relation=rel)
                print(f" Added: ({sub}) --[{rel}]--> ({obj})")
        except Exception as e:
            print(f"Skipped a line due to parsing constraints: {e}")

    # Persist the structured knowledge graph to disk layout
    nx.write_gexf(G, "./knowledge_graph.gexf")
    print("\n✅ Knowledge Graph successfully built and serialized to disk!")

if __name__ == "__main__":
    build_knowledge_graph()