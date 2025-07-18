from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from config import Config
import os

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    socketio.init_app(app)

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    # Register Blueprints
    from routes.chat_routes import chat_bp
    app.register_blueprint(chat_bp)

    return app,socketio

