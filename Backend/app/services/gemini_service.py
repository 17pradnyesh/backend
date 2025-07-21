import google.generativeai as genai
import json
import os
from app.config import Config

# Load system instructions from file
if not os.path.exists(Config.INSTRUCTIONS_PATH):
    raise FileNotFoundError(f"Instructions file not found at {Config.INSTRUCTIONS_PATH}")

try:
    with open(Config.INSTRUCTIONS_PATH, "r", encoding="utf-8") as f:
        SYSTEM_INSTRUCTIONS = json.load(f)
except json.JSONDecodeError as e:
    raise ValueError(f"Invalid JSON in {Config.INSTRUCTIONS_PATH}: {e}")

# Configure Gemini API key
if not Config.GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing in config")

genai.configure(api_key=Config.GOOGLE_API_KEY)

# Session store
sessions = {}

def start_session(sid, persona="realist_doctor"):
    if persona not in SYSTEM_INSTRUCTIONS:
        raise ValueError(
            f"Persona '{persona}' not found in instructions. Available personas: {list(SYSTEM_INSTRUCTIONS.keys())}"
        )
    
    system_instruction = SYSTEM_INSTRUCTIONS[persona]

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 1.2,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            },
            system_instruction=system_instruction
        )
        print('Model created for persona : ',persona)
    except Exception as e:
        print(f"Error creating Gemini model for persona '{persona}': {e}")
        raise

    chat = model.start_chat(history=[])
    sessions[sid] = chat
    print('Chat started for persona : ',persona)
   
    return chat

def get_session(sid):
    return sessions.get(sid)

def end_session(sid):
    if sid in sessions:
        del sessions[sid]

# Optional: Test function to validate all personas load properly
def test_personas():
    print("Testing available personas:")
    for persona in SYSTEM_INSTRUCTIONS:
        print(f"  - Testing persona: {persona}")
        try:
            chat = start_session("test_sid", persona)
            print("    Success")
        except Exception as e:
            print(f"    Failed with error: {e}")

if __name__ == "__main__":
    test_personas()
