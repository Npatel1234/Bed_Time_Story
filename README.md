Bedtime Stories App
Welcome to the Bedtime Stories App, an interactive storytelling engine that lets users shape immersive narratives through choices, powered by AI. Set in themes like sci-fi, fantasy, or haunted mysteries, the app delivers vivid, novel-like stories with dynamic characters, text-to-speech narration, and a sleek, sci-fi-themed web interface.
Features

Interactive Storytelling: Make choices to guide the story, with each decision advancing the narrative in a cohesive, engaging way.
AI-Powered Narratives: Uses a local Mistral 7B model (via LM Studio) to generate rich, premise-specific stories with vivid sensory details.
Dynamic Characters: Premise-tailored characters (e.g., Clara the detective for mysteries) drive the story with actions and dialogue.
Text-to-Speech (TTS): Optional narration of each story segment using gTTS, with audio playback in the browser.
Responsive Frontend: A modern, sci-fi-themed UI built with HTML, CSS (Tailwind), and JavaScript, featuring a starry background, neon animations, and a loading spinner.
Persistent State: Stores story events, characters, and progress in a SQLite database for continuity.
Loading Animation: Displays a pulsating neon ring during story generation for a smooth user experience.

Project Structure
bedtime_stories_app/
├── app.py                  # Flask backend with storytelling logic
├── templates/
│   └── index.html          # Frontend HTML with Tailwind CSS
├── static/
│   └── script.js           # JavaScript for API calls and UI updates
└── world_state.db          # SQLite database (created at runtime)

Prerequisites

Python 3.8+: For running the Flask backend.
LM Studio: Local server for Mistral 7B model (runs on http://localhost:1234).
Node.js: Optional, for local development tools (not required for core app).
Git: For cloning the repository.

Installation

Clone the Repository:
git clone https://github.com/your-username/bedtime_stories_app.git
cd bedtime_stories_app


Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install flask flask-cors gtts requests


Install LM Studio:

Download and install LM Studio.
Load a Mistral 7B model and start the local server at http://localhost:1234.



Running the App

Start the Backend:
python app.py

The app will run on http://localhost:5000.

Access the App:

Open http://localhost:5000 in a web browser.
Select a story premise (e.g., “Mystery in a haunted mansion”).
Toggle TTS (optional) and click “Start Story” to begin.
Make choices to advance the narrative, with audio narration (if enabled).



Usage

Start a Story: Choose a premise from the dropdown and click “Start Story” or “Reset Story” to begin or restart.
Make Choices: Select from three dynamic choices to shape the story, each with clear narrative consequences.
Text-to-Speech: Enable TTS for audio narration of each story segment, played via a custom audio player.
Responsive UI: Enjoy a sci-fi-themed interface with a starry background, neon buttons, and a loading animation during story generation.
Story Persistence: The SQLite database (world_state.db) tracks events, characters, and progress for a continuous experience.

Example Output
**System:** Embarking on a Mystery in a haunted mansion

**Narrator:** Clara, the sharp-witted detective, stepped cautiously into the haunted mansion, her flashlight casting eerie shadows on the cracked walls. The air was thick with the musty scent of decay, and a faint whisper seemed to echo from the grand staircase. As she approached an ancient portrait of a woman with piercing eyes, Clara felt a chill run down her spine, as if the painting were alive. “There’s something off about this place,” she muttered, her voice steady despite the creeping dread. The portrait’s gaze seemed to beckon her closer, hinting at secrets buried within the mansion’s past. Somewhere in the distance, a floorboard creaked, suggesting she wasn’t alone.

**System:** What will you do next?
1. Examine the portrait for hidden clues
2. Follow the creaking sound upstairs
3. Search the nearby bookcase for secrets

Troubleshooting

Error: “No such table: events”:
Delete world_state.db and restart the app to recreate the database.
Ensure init_db is called before database operations (fixed in the latest app.py).


Error: “NameError: new_progress is not defined”:
Use the latest app.py, which defines new_progress before database updates.


LM Studio Connection Issues:
Verify LM Studio is running at http://localhost:1234.
Check logs for API errors (app.logger.error).


UI Not Updating:
Open the browser console (F12) to check for JavaScript errors.
Ensure /start and /choice endpoints return valid JSON.



Security Considerations

Input Sanitization: Predefined premises prevent prompt injection, but sanitize custom premises if added.
CORS: In production, restrict CORS to the frontend origin (CORS(app, origins=["http://your-domain"])).
API Security: Add rate limiting and authentication for /start and /choice endpoints in production.
Database: Protect world_state.db from unauthorized access in production environments.

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request with a description of your changes.

Please include tests and update documentation for new features.
Future Enhancements

Custom Premises: Allow users to input custom story premises with input validation.
Themed UI: Adapt the frontend style (e.g., gothic for mystery, medieval for fantasy) based on the premise.
Story Branching: Track choice consequences in the database for deeper narrative paths.
Enhanced Audio: Add background sound effects (e.g., creaking floors) using a library like pydub.
Error UI: Display server errors (e.g., database failures) in the frontend story container.


Built with Flask, Tailwind CSS, and gTTS.
Powered by LM Studio for local AI inference.
Inspired by interactive fiction and AI-driven storytelling.


Happy Storytelling!For issues or feature requests, open a GitHub issue or contact [your-username].
