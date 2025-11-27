# 🎓 MS Application Agent

An intelligent, AI-powered assistant that helps students plan their Master's degree applications. This agentic workflow automates the entire process from profile analysis to generating a personalized application timeline.

## ✨ Features

### 🤖 Multi-Agent Architecture
A team of 5 specialized AI agents working in harmony:
1.  **Profile Intake Agent**: Analyzes student background and preferences
2.  **Program Search Agent**: Finds the best matching universities
3.  **Requirements Parser Agent**: Scrapes and extracts real admission requirements
4.  **Timeline Planner Agent**: Creates intelligent, backward-planned application schedules
5.  **Checklist Validator Agent**: Validates timeline and provides friendly, actionable warnings

### 🎯 Smart Features
- **⚡ Real-Time Streaming**: Watch the agents work in real-time via Server-Sent Events (SSE)
- **🎨 Modern UI/UX**: Premium glassmorphism design with:
  - Welcome onboarding screen
  - Multi-step form with validation
  - Responsive sidebar navigation
  - Interactive agent flow visualization
  - Clean program cards with timeline display
- **🔍 Real Data**: Web scraping of actual university admission pages
- **🧠 Intelligent Timeline Planning**:
  - Automatic deadline validation
  - Detects if intake deadline has passed
  - Auto-adjusts to next intake cycle if needed
  - Ensures all task dates are realistic and in the future
  - Backward planning from application deadline
- **👥 User-Friendly Warnings**: Clear, actionable advice with emojis (no technical jargon)
- **📱 Fully Responsive**: Works seamlessly on desktop, tablet, and mobile

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI/LLM**: Google Gemini API (`gemini-2.5-flash`)
- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
- **Data Processing**: Dataclasses, BeautifulSoup4
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

1.  **Onboarding**: Welcome screen explains the process in 3 simple steps
2.  **User Input**: Multi-step form collects your profile, preferences, and test scores
3.  **Real-Time Processing**: Watch AI agents work:
    - **Profile Agent**: Structures your data
    - **Search Agent**: Finds matching programs via AI reasoning
    - **Requirements Agent**: Scrapes university websites for real requirements
    - **Timeline Agent**: Creates backward-planned schedule with intelligent deadline detection
    - **Validator Agent**: Reviews timeline and provides friendly warnings
4.  **Smart Results**: 
    - Auto-detects if deadlines have passed
    - Adjusts to next intake cycle if needed
    - Provides realistic, chronological task timeline
    - Displays friendly warnings with actionable advice

## 🤝 Built With Google Antigravity

This project's frontend and agentic architecture were rapidly prototyped and implemented using **Google Antigravity**, an advanced AI coding assistant. Antigravity helped with:
- Designing the glassmorphism UI
- Implementing the real-time SSE streaming logic
- Debugging complex Pydantic serialization issues
- Structuring the multi-agent Python backend

## 📄 License

MIT License
