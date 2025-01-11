from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from backend import process_chat_message

app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist')
CORS(app)

@app.route('/')
def frontpage_index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    response = process_chat_message(user_message, session_id)
    
    return jsonify({'response': response})

@app.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('.', filename)