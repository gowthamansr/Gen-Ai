# backend.py
import os
import networkx as nx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from pyvis.network import Network

load_dotenv()

# =====================================================================
# GRAPH RETRIEVAL PATTERN CONFIGURATION
# =====================================================================
GRAPH_PATH = "./knowledge_graph.gexf"

def generate_graph_html(destination: str) -> str:
    """
    Finds matching nodes and writes out an interactive, 
    physically modeled localized HTML graph network chart.
    """
    if not os.path.exists(GRAPH_PATH):
        return ""
        
    # Read the data file
    G = nx.read_gexf(GRAPH_PATH)
    
    # Isolate target entity term match variants
    target = destination.split(",")[0].strip().lower()
    matched_nodes = [node for node in G.nodes if target in str(node).lower()]
    
    if not matched_nodes:
        return ""
        
    # Build a small localized display subgraph of matching items and connections
    subgraph_nodes = set(matched_nodes)
    for node in matched_nodes:
        subgraph_nodes.update(G.successors(node))
        subgraph_nodes.update(G.predecessors(node))
        
    sub_G = G.subgraph(subgraph_nodes)
    
    # Initialize the Pyvis interactive visual view
    # notebook=False prevents JavaScript loading collisions inside Streamlit
    net = Network(height="400px", width="100%", bgcolor="#ffffff", font_color="#333333", directed=True)
    
    # Translate NetworkX metrics natively over to Pyvis nodes
    for node, attrs in sub_G.nodes(data=True):
        # Apply visual distinct highlights to the target query term node
        if any(target in str(node).lower() for target in [target]):
            net.add_node(node, label=str(node), color="#ff4b4b", size=25, title="Search Match Target Pivot")
        else:
            net.add_node(node, label=str(node), color="#1f77b4", size=18, title="Connected Graph Entity")
            
    # Map edges across
    for source, target_node, edge_attrs in sub_G.edges(data=True):
        relationship_label = edge_attrs.get("relation", "linked")
        net.add_edge(source, target_node, label=relationship_label, color="#aaaaaa", arrows="to")
        
    # Return the raw string container configuration
    return net.generate_html()

def get_graph_context(destination: str) -> str:
    """Traverses the NetworkX structure using case-insensitive partial matching."""
    if not os.path.exists(GRAPH_PATH):
        return "Warning: No Knowledge Graph index file discovered on local storage."
        
    G = nx.read_gexf(GRAPH_PATH)
    retrieved_facts = []
    
    # 1. Normalize the search target (e.g., "paris")
    target = destination.split(",")[0].strip().lower()
    
    # 2. Advanced Partial Match: Find any node that CONTAINS the user's input string
    matched_nodes = [node for node in G.nodes if target in str(node).lower()]
    
    print(f"DEBUG: Target term '{target}' matched graph nodes: {matched_nodes}")
    
    # 3. Pull relations for all matched nodes
    for node in matched_nodes:
        # Pull outgoing edges (e.g., Paris -> CLOSED_ON -> Tuesday)
        for successor in G.successors(node):
            rel_data = G.get_edge_data(node, successor)
            retrieved_facts.append(f"- {node} {rel_data.get('relation', 'related to')} {successor}")
            
        # Pull incoming edges (e.g., Parc de Belleville -> LOCATED_IN -> Paris)
        for predecessor in G.predecessors(node):
            rel_data = G.get_edge_data(predecessor, node)
            retrieved_facts.append(f"- {predecessor} {rel_data.get('relation', 'related to')} {node}")
            
    if not retrieved_facts:
        return f"No explicit graph network relations matched your target entity variants for '{destination}'."
        
    return "\n".join(set(retrieved_facts))

# Guardrail & Model initializations remain secure
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
guardrail_judge = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

judge_prompt = ChatPromptTemplate.from_messages([
    ("system", "Evaluate if the user's prompt is a travel request. Output EXACTLY 'ALLOWED' or 'BLOCKED'."),
    ("user", "Destination: {destination}. Days: {days}")
])
guardrail_chain = judge_prompt | guardrail_judge | StrOutputParser()

travel_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert travel guide. Build a detailed itinerary.\n"
        "You MUST align your response perfectly with the structural Graph-Network Relationships "
        "extracted below. Treat these entity mappings as unbreakable hard truths.\n\n"
        "Graph Relations Context:\n{context}"
    )),
    ("user", "I want to visit {destination} for {days} days.")
])
generation_chain = travel_prompt | llm | StrOutputParser()

# =====================================================================
# INTERFACE EXPOSURE CHANNELS
# =====================================================================
def run_input_guardrails(destination: str, days: str) -> tuple[bool, str]:
    if not destination.strip() or not days.strip():
        return False, "⚠️ Fields cannot be blank."
    clean_days = ''.join(filter(str.isdigit, days))
    if not clean_days or int(clean_days) <= 0 or int(clean_days) > 30:
        return False, "🛑 Invalid day ranges entered."
        
    decision = guardrail_chain.invoke({"destination": destination, "days": clean_days})
    if decision.strip() != "ALLOWED":
        return False, "🛑 Guardrail Interception: Travel queries only."
    return True, clean_days

def generate_itinerary_stream(destination: str, days: str, context: str):
    payload = {"destination": destination, "days": days, "context": context}
    for chunk in generation_chain.stream(payload):
        yield chunk

def run_deepeval_audit(destination: str, days: str, actual_output: str):
    user_query = f"Create a {days}-day itinerary for {destination}."
    test_case = LLMTestCase(input=user_query, actual_output=actual_output)
    relevancy_metric = AnswerRelevancyMetric(threshold=0.7, model="gpt-4o-mini")
    relevancy_metric.measure(test_case)
    return {
        "score": relevancy_metric.score,
        "passed": relevancy_metric.is_successful(),
        "reason": relevancy_metric.reason
    }