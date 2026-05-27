import os
#  This is the modern, modular way
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 0. Set up your API key (Replace with your actual OpenAI key)
os.environ["OPENAI_API_KEY"] = "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"

# =====================================================================
# 1. THE PROMPT
# =====================================================================
# We define a template with a placeholder variable {topic}. 
# This ensures the LLM gets consistent instructions every time.
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a hilarious comedian. Tell a short, witty joke about the requested topic."),
    ("human", "Tell me a joke about {topic}.")
])

# =====================================================================
# 2. THE MODEL I/O
# =====================================================================
# This initializes our connection to the language model. 
# We use 'temperature=0.7' to give the AI a bit of creative flair for comedy.
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# =====================================================================
# 3. THE OUTPUT PARSER
# =====================================================================
# By default, LLMs return a complex object containing metadata (like token usage).
# The StrOutputParser extracts just the raw text response from the model.
output_parser = StrOutputParser()

# =====================================================================
# 4. THE CHAIN
# =====================================================================
# This is where the magic happens. We link the components together using 
# LangChain Expression Language (LCEL) via the pipe operator (|).
# Data flows from: Prompt -> Model -> Output Parser
joke_chain = prompt_template | model | output_parser

# =====================================================================
# RUNNING THE APPLICATION
# =====================================================================
# We invoke the chain and pass in the variable for our prompt template.
if __name__ == "__main__":
    topic_input = "lion"
    
    print(f"Sending topic '{topic_input}' through the chain...\n")
    response = joke_chain.invoke({"topic": topic_input})
    
    print("--- AI Response ---")
    print(response)