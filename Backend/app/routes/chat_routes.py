from flask import Blueprint, request, render_template
from flask_socketio import emit
# from app import socketio
from services import gemini_service, file_service
from app_initializer import socketio

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/")
def index():
    return render_template("index2.html")

@socketio.on("connect")
def handle_connect():
    sid = request.sid
    persona = request.args.get("persona", "root_doctor")
    print('Persona received : ',persona)
    gemini_service.start_session(sid, persona)
    print('Session started : ',sid)
    emit("connected", {"message": "WebSocket connected and chat session started."})

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    gemini_service.end_session(sid)
    print(f"Session {sid} disconnected.")

@socketio.on("chat_message")
def handle_message(data):
    sid = request.sid
    chat = gemini_service.get_session(sid)

    if not chat:
        print('Chat session not found : ',sid)
        emit("error", {"error": "Chat session not found."})
        return

    prompt = data.get("prompt", "").strip()
    print('Prompt received : ',prompt)
    file_data = data.get("file_data")
    filename = data.get("filename")
    mimetype = data.get("mimetype")
    inputs = []

    try:
        if filename and file_data:
            uploaded_file, error = file_service.handle_file_upload_base64(file_data, filename, mimetype)
            if error:
                emit("error", {"error": error})
                return
            if not prompt:
                prompt = "Transcribe and understand the content of the file."
            inputs = [uploaded_file, prompt]
        else:
            inputs = [prompt]

        print('Inputs : ',inputs)
        result = chat.send_message(inputs)
        emit("bot_response", {
            "type": "bot_response",
            "response": result.text.strip()
        })
    except Exception as e:
        print('Exception : ',e)
        emit("error", {"error": f"Gemini error: {str(e)}"})
