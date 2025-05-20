# 🌌 Bedtime Stories App

Welcome to the **Bedtime Stories App**, an immersive, interactive storytelling engine powered by AI. Designed with sci-fi aesthetics and a sleek UI, this app lets users shape vivid narratives by making choices—each branching into a unique story arc. With dynamic characters, real-time text-to-speech (TTS) narration, and smooth UI animations, it brings bedtime storytelling to the next level.

---

## ✨ Features

- **🧭 Interactive Storytelling:** Player choices guide the plot through custom AI-generated scenes.
- **🧠 AI-Powered Narratives:** Uses a local **Mistral 7B** model (via LM Studio) to generate rich, immersive storylines.
- **🎭 Dynamic Characters:** Premise-specific personalities engage in dialogue and drive the story forward.
- **🔊 Text-to-Speech (TTS):** Optional narration of story passages using **gTTS** (or your preferred TTS model).
- **💫 Responsive Frontend:** A futuristic UI with neon accents, animations, and a starry background.
- **📜 Persistent State:** Uses a SQLite database to track progress, characters, and plot history.
- **💡 Loading Animation:** Neon spinner appears during AI generation for smooth UX.

---

## 📁 Project Structure

```
bedtime_stories_app/
├── Story.py                 # Backend (Flask)
├── world_state.db         # SQLite database
├── static/                
├── templates/             
├── README.md
└── requirements.txt
```
---

## 🛠️ Prerequisites

- **Python 3.8+**
- **LM Studio** (running Mistral 7B at `http://localhost:1234`)
- **Git**
- **gTTS or Kokoro TTS** (installed for narration)

---

## 🚀 Installation

```bash
# 1. Clone the repo

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt
