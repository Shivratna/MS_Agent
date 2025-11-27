# 🎓 MS Application Agent

An intelligent, AI-powered assistant that helps students plan their Master's degree applications. This agentic workflow automates the entire process from profile analysis to generating a personalized application timeline.

![MS Agent UI](https://via.placeholder.com/800x400?text=MS+Application+Agent+UI)

## ✨ Features

- **🤖 Multi-Agent Architecture**: A team of 5 specialized AI agents working in harmony:
  1.  **Profile Intake Agent**: Analyzes student background and preferences.
  2.  **Program Search Agent**: Finds the best matching universities.
  3.  **Requirements Parser Agent**: Scrapes and extracts real admission requirements.
  4.  **Timeline Planner Agent**: Creates a backward-planned application schedule.
  5.  **Checklist Validator Agent**: Ensures all deadlines and requirements are met.

- **⚡ Real-Time Streaming**: Watch the agents "think" and work in real-time via Server-Sent Events (SSE).
- **🎨 Premium UI**: A beautiful, glassmorphism-inspired interface built with **Google Antigravity**.
- **🔍 Real Data**: Uses `googlesearch-python` and `beautifulsoup4` to fetch live admission data from university websites.
- **📱 Responsive Design**: Works seamlessly on desktop and mobile.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI/LLM**: Google Gemini API (`gemini-2.5-flash`)
- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
- **Data Processing**: Pydantic, BeautifulSoup4
- **Development**: Built with **Google Antigravity** (Advanced Agentic Coding)

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A Google Gemini API Key

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/MS_Agent.git
    cd MS_Agent
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**
    Create a `.env` file in the root directory:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

### Running the App

1.  **Start the server**
    ```bash
    uvicorn server:app --reload
    ```

2.  **Open your browser**
    Navigate to `http://localhost:8000`

## 🧠 How It Works

The system uses an **Orchestrator** pattern to manage the flow of data between agents:

1.  **User Input**: You provide your GPA, interests, and target countries.
2.  **Agent Workflow**:
    - The *Profile Agent* structures your data.
    - The *Search Agent* finds programs.
    - The *Requirements Agent* visits university pages to get real data.
    - The *Timeline Agent* calculates dates based on deadlines.
    - The *Validator Agent* double-checks everything.
3.  **Result**: You get a structured, interactive plan with a timeline and warnings.

## 🤝 Built With Google Antigravity

This project's frontend and agentic architecture were rapidly prototyped and implemented using **Google Antigravity**, an advanced AI coding assistant. Antigravity helped with:
- Designing the glassmorphism UI
- Implementing the real-time SSE streaming logic
- Debugging complex Pydantic serialization issues
- Structuring the multi-agent Python backend

## 📄 License

MIT License
