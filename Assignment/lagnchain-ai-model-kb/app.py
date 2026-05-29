from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Mahindra XUV700 AI Assistant",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.main-header {
    font-size: 2.5rem;
    font-weight: bold;
}

.sub-header {
    color: gray;
    margin-bottom: 20px;
}

.metric-card {
    padding: 10px;
    border-radius: 10px;
    background-color: #f5f5f5;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🚘 XUV700")

    st.markdown("---")

    st.markdown("### Assistant Features")

    st.markdown("""
    ✅ Specifications

    ✅ Features

    ✅ Safety

    ✅ Variants

    ✅ Technology

    ✅ Performance
    """)

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="main-header">Mahindra XUV700 AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-header">Ask questions directly from the brochure</div>',
    unsafe_allow_html=True
)

# =====================================================
# PDF CHECK
# =====================================================

PDF_FILE = "xuv700-sample.pdf"

if not os.path.exists(PDF_FILE):

    st.error(f"PDF file not found: {PDF_FILE}")

    st.stop()

# =====================================================
# LOAD RAG
# =====================================================

@st.cache_resource
def initialize_rag():

    loader = PyPDFLoader(PDF_FILE)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a Mahindra XUV700 product specialist.

Previous Conversation:
{history}

Brochure Context:
{context}

Customer Question:
{question}

Instructions:

- Use brochure information only.
- Mention specifications when available.
- Mention variant names if applicable.
- Be concise and professional.
- If answer is unavailable, say:
  "I could not find that information in the brochure."
"""
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    return retriever, chain, len(documents), len(chunks)


retriever, chain, page_count, chunk_count = initialize_rag()

# =====================================================
# STATS
# =====================================================

col1, col2 = st.columns(2)

with col1:
    st.metric("Pages Loaded", page_count)

with col2:
    st.metric("Knowledge Chunks", chunk_count)

st.markdown("---")

# =====================================================
# SUGGESTED QUESTIONS
# =====================================================

with st.expander("💡 Suggested Questions"):

    st.markdown("""
    - What engine options are available?
    - What ADAS features are included?
    - What safety features does the XUV700 offer?
    - What is the boot space?
    - Compare AX7 and AX7L.
    - What infotainment features are available?
    """)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content":
            """
Welcome to the Mahindra XUV700 AI Assistant.

Ask me anything about:

• Features
• Specifications
• Variants
• Safety
• Technology
• Performance
            """
        }
    ]

# =====================================================
# DISPLAY CHAT
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =====================================================
# USER INPUT
# =====================================================

question = st.chat_input(
    "Ask about XUV700..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    history_text = ""

    for msg in st.session_state.messages:

        history_text += (
            f"{msg['role']}: {msg['content']}\n"
        )

    retrieved_docs = retriever.invoke(question)

    context_text = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    source_pages = []

    for doc in retrieved_docs:

        if "page" in doc.metadata:

            source_pages.append(
                str(doc.metadata["page"] + 1)
            )

    with st.chat_message("assistant"):

        with st.spinner("Searching brochure..."):

            answer = chain.invoke(
                {
                    "history": history_text,
                    "context": context_text,
                    "question": question
                }
            )

        st.markdown(answer)

        if source_pages:

            st.caption(
                f"📄 Source Pages: {', '.join(sorted(set(source_pages)))}"
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )