# Medical AI Skin Diagnosis System

A production-grade medical web application for AI-powered skin disease diagnosis.

## Tech Stack

- **Backend**: Python Flask (Modular Architecture)
- **Frontend**: Pure HTML/CSS/JavaScript (Mobile-first)
- **Storage**: JSON files with file locking
- **AI**: Multi-stage pipeline with fallback (OpenRouter, Groq, Gemini)

## Quick Start

### 1. Setup Environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```
OPENROUTER_API_KEY=your_key
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
SECRET_KEY=your_secret_key
```

### 3. Run the Application

```bash
python app.py
```

Open `http://localhost:5002` in your browser.

## Project Structure

```
SkinApp/
├── backend/          # Flask API server
├── frontend/         # HTML/CSS/JS files
└── data/            # JSON data storage
```

## Features

- Multi-stage AI diagnosis pipeline
- Patient & Doctor portals
- Admin management panel
- Wallet-based payments
- RAG AI Assistant
- Arabic/English support
- Dark/Light themes
