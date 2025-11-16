import streamlit as st
from src.query import query_store
from langchain_ollama import ChatOllama

st.set_page_config(page_title="Chat with PDFs", page_icon="📄")

st.title("📄 Chat with your PDFs")

# User question
user_q = st.text_input("Ask a question about your PDF:")

if user_q:
    st.write("🔍 Searching relevant chunks...")

    # Retrieve relevant text chunks
    chunks = query_store(user_q, k=3)

    context = "\n\n".join(chunks)

    st.write("🧠 Generating answer...")

    # Ask Mistral via Ollama
    llm = ChatOllama(model="mistral")

    prompt = f"""
    Answer the question using *only* the context below.
    If the answer isn't in the context, say "I cannot find that in the PDF."

    Context:
    {context}

    Question:
    {user_q}
    """

    response = llm.invoke(prompt)
    st.write(response.content)
