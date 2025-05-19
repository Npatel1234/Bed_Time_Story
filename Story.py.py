import flask
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import sqlite3
import json
import time
from uuid import uuid4
from gtts import gTTS
import os
import base64
import logging

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# LM Studio API configuration
LM_STUDIO_API_URL = "http://localhost:1234/v1/completions"

# Initialize SQLite database for world state
def init_db(premise):
    try:
        with sqlite3.connect("world_state.db") as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS events
                         (id TEXT PRIMARY KEY, description TEXT, timestamp INTEGER)''')
            c.execute('''CREATE TABLE IF NOT EXISTS characters
                         (id TEXT PRIMARY KEY, name TEXT, traits TEXT, premise TEXT)''')
            c.execute('''CREATE TABLE IF NOT EXISTS world
                         (key TEXT PRIMARY KEY, value TEXT)''')
            # Initialize premise-specific character
            character = get_premise_character(premise)
            c.execute("INSERT OR REPLACE INTO characters (id, name, traits, premise) VALUES (?, ?, ?, ?)",
                      (str(uuid4()), character["name"], character["traits"], premise))
            # Initialize story progress
            c.execute("INSERT OR REPLACE INTO world (key, value) VALUES (?, ?)",
                      ("progress", "introduction"))
            conn.commit()
    except sqlite3.Error as e:
        app.logger.error(f"Database initialization error: {e}")
        raise

# Define premise-specific characters
def get_premise_character(premise):
    characters = {
        "Sci-fi adventure on a desert planet": {"name": "Kael", "traits": "fearless starpilot with a knack for uncovering ancient tech"},
        "Fantasy quest in a magical kingdom": {"name": "Elara", "traits": "courageous mage with a mysterious past"},
        "Mystery in a haunted mansion": {"name": "Clara", "traits": "sharp-witted detective with a fascination for the occult"}
    }
    return characters.get(premise, {"name": "Clara", "traits": "sharp-witted detective"})

# Helper function to query Mistral 7B via LM Studio API
def query_model(prompt, max_tokens=300):
    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 0.9,
        "do_sample": True
    }
    try:
        response = requests.post(LM_STUDIO_API_URL, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
    except requests.RequestException as e:
        app.logger.error(f"LM Studio API error: {e}")
        return f"Error querying model: {e}"

# Text-to-Speech function
def text_to_speech(text, output_file="output.mp3"):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(output_file)
        with open(output_file, "rb") as f:
            audio_data = base64.b64encode(f.read()).decode('utf-8')
        os.remove(output_file)
        return audio_data
    except Exception as e:
        app.logger.error(f"TTS error: {e}")
        return None

# Unified Narrative Generator
def generate_narrative(premise, user_choice, world_state, history, character):
    progress = world_state.get("progress", "introduction")
    history_str = "\n".join([f"{speaker}: {text}" for speaker, text in history[-5:]])
    prompt = f"""
You are a master storyteller crafting an immersive, engaging narrative in the {premise} setting. The current story progress is '{progress}'.
Previous story events:
{history_str}
World state: {json.dumps(world_state)}.
User choice: {user_choice or "Begin the story"}.
Character: {character['name']}, a {character['traits']}.

Write a cohesive narrative paragraph (4-6 sentences) in third-person, past tense, that:
- Advances the story with a new event or conflict, building on the user's choice.
- Includes vivid sensory details (sights, sounds, smells) to set the scene.
- Features {character['name']} taking action or speaking, reflecting their traits.
- Maintains a tone consistent with the premise (e.g., eerie for mystery, epic for fantasy).
- Foreshadows future challenges or mysteries.
Ensure the narrative feels like a continuous, gripping story, connecting to past events and the user's choice.
"""
    narrative = query_model(prompt, max_tokens=400)
    # Update progress
    new_progress = "rising_action" if progress == "introduction" else "climax" if progress == "rising_action" else "resolution"
    app.logger.debug(f"Updating story progress to: {new_progress}")
    try:
        with sqlite3.connect("world_state.db") as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO world (key, value) VALUES (?, ?)", ("progress", new_progress))
            c.execute("INSERT INTO events (id, description, timestamp) VALUES (?, ?, ?)",
                      (str(uuid4()), narrative, int(time.time())))
            conn.commit()
    except sqlite3.Error as e:
        app.logger.error(f"Error updating narrative in database: {e}")
    return narrative

# User Interaction Agent (generates choice options)
def user_interaction_agent(premise, context, world_state):
    progress = world_state.get("progress", "introduction")
    prompt = f"""
You are a choice generator for a {premise} story. Current story progress: '{progress}'.
Context: {context}.
World state: {json.dumps(world_state)}.

Generate 3 distinct, concise choice options (each 8-12 words) for the user's next action. Each choice should:
- Be specific to the context and premise.
- Have clear narrative consequences (e.g., exploration, confrontation, investigation).
- Reflect the story's tone (e.g., eerie for mystery).
Format as a JSON list: ["Choice 1", "Choice 2", "Choice 3"]
"""
    result = query_model(prompt, max_tokens=150)
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return ["Investigate further", "Confront the mystery", "Seek an escape"]

# Main storytelling logic
def storytelling_engine(premise, user_choice=None, reset=False, tts_enabled=True):
    if not hasattr(storytelling_engine, "history") or reset:
        storytelling_engine.history = []
        storytelling_engine.premise = premise
        storytelling_engine.choices = []
        try:
            init_db(premise)  # Ensure tables exist before DELETE
            with sqlite3.connect("world_state.db") as conn:
                c = conn.cursor()
                c.execute("DELETE FROM events")
                c.execute("DELETE FROM characters")
                c.execute("DELETE FROM world")
                conn.commit()
            init_db(premise)  # Re-initialize with character and progress
        except sqlite3.Error as e:
            app.logger.error(f"Error resetting database: {e}")
            return {"error": "Database error during reset"}, 500

    history = storytelling_engine.history
    premise = storytelling_engine.premise

    try:
        with sqlite3.connect("world_state.db") as conn:
            c = conn.cursor()
            c.execute("SELECT key, value FROM world")
            world_state = {row[0]: row[1] for row in c.fetchall()}
            c.execute("SELECT name, traits FROM characters WHERE premise = ?", (premise,))
            row = c.fetchone()
            if not row:
                init_db(premise)  # Re-initialize if character missing
                c.execute("SELECT name, traits FROM characters WHERE premise = ?", (premise,))
                row = c.fetchone()
            character = {"name": row[0], "traits": row[1]}
    except sqlite3.Error as e:
        app.logger.error(f"Error accessing database: {e}")
        return {"error": "Database access error"}, 500

    audio_data = None
    narrative = ""
    if not history:
        history.append(("System", f"Embarking on a {premise}"))
        narrative = generate_narrative(premise, "", world_state, history, character)
        history.append(("Narrator", narrative))
        storytelling_engine.choices = user_interaction_agent(premise, narrative, world_state)
        history.append(("System", "What will you do next?"))
        if tts_enabled:
            audio_data = text_to_speech(narrative, "initial_narrative.mp3")
    elif user_choice:
        history.append(("User", user_choice))
        narrative = generate_narrative(premise, user_choice, world_state, history, character)
        history.append(("Narrator", narrative))
        storytelling_engine.choices = user_interaction_agent(premise, narrative, world_state)
        history.append(("System", "What will you do next?"))
        if tts_enabled:
            audio_data = text_to_speech(narrative, "narrative_update.mp3")

    chat_output = ""
    for speaker, text in history:
        if speaker == "System" and "next" in text.lower():
            chat_output += f"**{speaker}:** {text}\n"
            for i, choice in enumerate(storytelling_engine.choices, 1):
                chat_output += f"{i}. {choice}\n"
            chat_output += "\n"
        else:
            chat_output += f"**{speaker}:** {text}\n\n"

    return {
        "chat_output": chat_output,
        "choices": storytelling_engine.choices,
        "audio": audio_data
    }

# API Endpoints
@app.route('/')
def index():
    return send_file('templates/index.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    premise = data.get('premise', "Mystery in a haunted mansion")
    tts_enabled = data.get('tts_enabled', True)
    result = storytelling_engine(premise, reset=True, tts_enabled=tts_enabled)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/choice', methods=['POST'])
def choice():
    data = request.json
    premise = data.get('premise', "Mystery in a haunted mansion")
    user_choice = data.get('choice')
    tts_enabled = data.get('tts_enabled', True)
    if user_choice:
        result = storytelling_engine(premise, user_choice=user_choice, tts_enabled=tts_enabled)
        if isinstance(result, dict) and "error" in result:
            return jsonify(result), 500
        return jsonify(result)
    return jsonify({"error": "No choice provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)