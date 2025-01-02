from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from detector import extract_details
from logic import generate_response
from context import initialize_chat_session, process_chat, get_detail_context

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
        chat_history[session_id] = initialize_chat_session()
    
    new_details = extract_details(user_message)
    current_details = chat_history[session_id]['details']
    current_details.update(new_details)
    chat_history[session_id]['details'] = current_details
    
    dialog_response = process_chat(user_message, chat_history[session_id])
    structured_response = generate_response(current_details, user_message)
    
    if "I need some more information" in structured_response:
        if dialog_response and len(dialog_response.strip()) >= 10:
            response = f"{dialog_response}\n\nBy the way, {structured_response.lower()}"
        else:
            response = structured_response
    else:
        if dialog_response and len(dialog_response.strip()) >= 10:
            response = f"{dialog_response}\n\nAlso, {structured_response}"
        else:
            response = structured_response
    
    chat_history[session_id]['dialog_history'].append(response)
    
    detail_context = get_detail_context(current_details)
    if detail_context:
        chat_history[session_id]['context'] += " " + ", ".join(detail_context) + "."

    return jsonify({'response': response})