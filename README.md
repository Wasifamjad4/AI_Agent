#  AI Agent

An intelligent web-powered AI agent that dynamically retrieves real-time information and synthesizes concise, context-aware responses using state-of-the-art LLMs via Groq's inference engine.

##  Features

-  Real-time web search via DuckDuckGo (no API key needed)
-  LLM-powered summarization using Groq (free tier)
-  Clickable sources showing where answers come from
-  Model selector to switch between Groq's free models
-  Answer style selector — Concise / Detailed / Explain like I'm 5
-  Raw search data inspector
-  Persistent chat history with clear chat option

## Tech Stack

| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | UI |
| [Groq](https://groq.com) | LLM inference (free tier) |
| [DDGS](https://pypi.org/project/ddgs/) | DuckDuckGo web search |
| Python 3.10+ | Core language |

##  Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/wasifamjad4/AI_Agent.git
cd AI_Agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the root folder:
GROQ_API_KEY=your-key-here

Get your free API key at [console.groq.com](https://console.groq.com).

### 5. Run the app

```bash
streamlit run app.py
```

##  Deployment

Deployed on Streamlit Community Cloud. To deploy your own instance:

1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `app.py` as the main file
4. Add `GROQ_API_KEY` under **Manage App → Settings → Secrets**

##  Project Structure

AI_Agent/
├── app.py            # Streamlit UI
├── agent.py          # CLI version of the agent
├── requirements.txt  # Python dependencies
├── .env              # API key (not pushed to GitHub)
└── .gitignore        # Excludes .env and venv/
