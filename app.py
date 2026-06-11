import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from ddgs import DDGS

load_dotenv()

st.title("AI Agent")
st.caption("Searches the web and summarizes the answer")

# --- Sidebar controls ---
with st.sidebar:
    st.header("Settings")

    model = st.selectbox("Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "qwen/qwen3-32b"

    ])

    num_results = st.slider("Number of search results", min_value=1, max_value=10, value=3)

    tone = st.radio("Answer style", [
        "Concise",
        "Detailed",
        "Explain like I'm 5"
    ])

    show_raw = st.toggle("Show raw search data", value=False)

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Tone to system prompt ---
tone_prompts = {
    "Concise": "You are a helpful assistant. Answer clearly and briefly in 2-3 sentences max.",
    "Detailed": "You are a helpful assistant. Give a thorough, well-structured answer with as much useful detail as possible.",
    "Explain like I'm 5": "You are a helpful assistant. Explain the answer in very simple language as if talking to a 5 year old. Use simple words and short sentences."
}

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render chat history ---
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            st.button("Copy", key=f"copy_hist_{i}")
            if "query" in msg:
                st.caption(f"🔍 Searched for: `{msg['query']}`")
            if "sources" in msg:
                with st.expander("Sources", expanded=False):
                    for s in msg["sources"]:
                        st.markdown(f"- [{s['title']}]({s['url']})")
            if show_raw and "raw" in msg:
                with st.expander("Raw search data", expanded=False):
                    st.text(msg["raw"])

# --- Functions ---
def search_web(query: str, max_results: int = 3):
    results = []
    sources = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(f"- {r['title']}: {r['body']}")
            sources.append({"title": r["title"], "url": r["href"]})
    context = "\n".join(results) if results else "No results found."
    return context, sources

def ask_llm(question: str, context: str, model: str, tone: str) -> str:
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    chat = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": tone_prompts[tone]},
            {"role": "user", "content": f"Question: {question}\n\nSearch results:\n{context}"}
        ],
        max_tokens=512
    )
    return chat.choices[0].message.content

# --- Chat input ---
if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching the web..."):
            context, sources = search_web(prompt, max_results=num_results)
        with st.spinner("Thinking..."):
            answer = ask_llm(prompt, context, model, tone)

        st.write(answer)
        st.button("Copy", key=f"copy_latest_{len(st.session_state.messages)}")
        st.caption(f"Searched for: `{prompt}`")

        with st.expander("Sources"):
            for s in sources:
                st.markdown(f"- [{s['title']}]({s['url']})")

        if show_raw:
            with st.expander("Raw search data"):
                st.text(context)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
        "raw": context,
        "query": prompt
    })