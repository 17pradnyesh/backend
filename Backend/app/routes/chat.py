# app/routes/chat.py
from flask import Blueprint, request, jsonify

import uuid
from app.services.gemini_service import GeminiService
from app.repositories.session_repo import create_session, get_session_by_id, update_session

chat_bp = Blueprint('chat', __name__)
gemini_service = GeminiService()


@chat_bp.route('/api/sessions', methods=['POST'])
def create_session_route():
    data = request.json or {}
    # You can add more fields as needed
    session_id = str(uuid.uuid4())
    session_data = {
        "session_id": session_id,
        "description": data.get("description", ""),
        "is_active": True,
        "created_by": data.get("created_by", None)
    }
    inserted_id = create_session(session_data)
    session = get_session_by_id(session_id)
    return jsonify(session), 201


@chat_bp.route('/api/chat', methods=['POST'])
def send_message():
    data = request.json
    session_id = data.get('session_id')
    message = data.get('message')
    
    if not session_id or not message:
        return jsonify({'error': 'session_id and message are required'}), 400

    session = get_session_by_id(session_id)
    if not session:
        # Optionally, you can auto-create a session if not found
        session_data = {
            "session_id": session_id,
            "description": "",
            "is_active": True,
            "created_by": None
        }
        create_session(session_data)
        session = get_session_by_id(session_id)

    try:
        response = gemini_service.send_message(session_id, message)
        update_session(session_id, {})  # This will update the updated_at timestamp
        return jsonify({
            'response': response.text,
            'session_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500