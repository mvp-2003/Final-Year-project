from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from detector import extract_details
from logic import generate_response

app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist')
CORS(app)

chat_history = {}

@app.route('/')
def frontpage_index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    if session_id not in chat_history:
        chat_history[session_id] = {}
    
    new_details = extract_details(user_message)
    current_details = chat_history[session_id]
    
    # Update the current details with new information
    current_details.update(new_details)
    chat_history[session_id] = current_details
    
    response = generate_response(current_details, user_message)
    return jsonify({'response': response})