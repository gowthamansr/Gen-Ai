import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# =====================================================================
# 1. IMPORT YOUR MAIN APP LOGIC
# =====================================================================
# This mimics your core generation chain from Step 6
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
travel_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert travel guide. Create a highly customized, day-by-day itinerary."),
    ("user", "I want to visit {destination} for {days} days. Please give me a good itinerary.")
])
production_chain = travel_prompt | llm | StrOutputParser()

def run_production_app(destination: str, days: str) -> str:
    """Helper to simulate running the production chain and returning the full text."""
    return production_chain.invoke({"destination": destination, "days": days})


# =====================================================================
# 2. DEFINING THE EVALUATION JUDGE
# =====================================================================
evaluator_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0) # 0.0 temperature for strict grading

evaluation_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an objective Quality Assurance auditor. Your job is to grade a Trip Planner AI's output.\n"
        "Analyze the provided USER REQUEST and the generated AI RESPONSE based on two metrics:\n\n"
        "1. RELEVANCE (Score 1-5): Does the response detail the specific destination requested?\n"
        "2. COMPLETENESS (Score 1-5): Does the itinerary successfully cover the specific number of days requested?\n\n"
        "Provide your output exactly in this format:\n"
        "RELEVANCE SCORE: [number]\n"
        "COMPLETENESS SCORE: [number]\n"
        "REASONING: [one brief sentence explaining the score]"
    )),
    ("user", "USER REQUEST:\nDestination: {destination}, Days: {days}\n\nAI RESPONSE:\n{response}")
])

eval_chain = evaluation_prompt | evaluator_llm | StrOutputParser()


# =====================================================================
# 3. RUNNING THE EVALUATION TEST SUITE
# =====================================================================
# A test dataset of sample test cases (including an edge case)
test_dataset = [
    {"destination": "Tokyo, Japan", "days": "3"},
    {"destination": "Cairo, Egypt", "days": "5"},
    {"destination": "Mumbai", "days": "1"}
]

print("🚀 Starting automated evaluation run over test dataset...\n")

for i, test_case in enumerate(test_dataset, 1):
    dest = test_case["destination"]
    days = test_case["days"]
    
    print(f"Test Case #{i}: Planning for {dest} for {days} days...")
    
    # 1. Run the live production code
    actual_response = run_production_app(dest, days)
    
    # 2. Run the evaluator judge over the results
    grade_report = eval_chain.invoke({
        "destination": dest,
        "days": days,
        "response": actual_response
    })
    
    print(f"\n--- EVALUATION REPORT FOR CASE #{i} ---")
    print(grade_report)
    print("-" * 50, "\n")

print("✅ Evaluation complete.")