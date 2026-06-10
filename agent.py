import os
from groq import Groq
from ddgs import DDGS
from dotenv import load_dotenv
load_dotenv()

# --- Web search ---
def search_web(query: str, max_results: int = 3) -> str:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(f"- {r['title']}: {r['body']}")
    return "\n".join(results) if results else "No results found."

# --- Ask the LLM ---
def ask_llm(question: str, context: str) -> str:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Use the provided search results to answer the user's question clearly and concisely."
            },
            {
                "role": "user",
                "content": f"Question: {question}\n\nSearch results:\n{context}"
            }
        ],
        max_tokens=512
    )
    return chat.choices[0].message.content

# --- Main agent loop ---
def run_agent():
    print(" AI Agent ready! Type 'quit' to exit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit"):
            print("Bye!")
            break
        if not question:
            continue

        print(" Searching the web...")
        search_results = search_web(question)

        print(" Thinking...\n")
        answer = ask_llm(question, search_results)

        print(f"Agent: {answer}\n")
        print("-" * 50 + "\n")

if __name__ == "__main__":
    run_agent()