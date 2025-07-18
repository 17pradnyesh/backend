import os
import base64
import uuid
from werkzeug.utils import secure_filename
from config import Config
import google.generativeai as genai

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def handle_file_upload_base64(file_data, file_name, mimetype):
    filename = secure_filename(str(uuid.uuid4()) + "_" + file_name)
    image_bytes = base64.b64decode(file_data)
    temp_path = os.path.join(Config.UPLOAD_FOLDER, filename)

    with open(temp_path, "wb") as f:
        f.write(image_bytes)

    try:
        uploaded = genai.upload_file(temp_path, mime_type=mimetype)
        os.remove(temp_path)
        return uploaded, None
    except Exception as e:
        return None, f"Upload failed: {str(e)}"
