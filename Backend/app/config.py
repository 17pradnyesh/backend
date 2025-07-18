# app/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    # Flask
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'dev-key-123')
    UPLOAD_FOLDER = 'temp_uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'ogg', 'wav', 'mp3', 'webm'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    BASE_DIR = Path(__file__).parent
    INSTRUCTIONS_PATH = str(BASE_DIR / 'system_instructions.json')
    
    # Session
    SESSION_LIFETIME = 3600  # 1 hour