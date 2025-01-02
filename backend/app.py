from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from detector import extract_details
from logic import generate_response
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist')
CORS(app)

chat_history = {}
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

initial_prompts = [
    "Hello! How can I assist you with identifying the suspect?",
    "I'm here to help you describe the suspect. What can you tell me?",
    "Welcome! I'll help you document the suspect's details. What information do you have?",
    "Hi there! I'm ready to help identify the suspect. What details can you share?",
]

@app.route('/')
def frontpage_index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    if session_id not in chat_history:
        chat_history[session_id] = {
            'details': {},
            'dialog_history': [],
            'context': "You are a helpful assistant collecting information about a suspect. Be friendly and engaging."
        }
    
    new_details = extract_details(user_message)
    current_details = chat_history[session_id]['details']
    current_details.update(new_details)
    chat_history[session_id]['details'] = current_details
    
    dialog_history = chat_history[session_id]['dialog_history']
    context = chat_history[session_id]['context']
    
    if not dialog_history:
        input_text = context
    else:
        dialog_history.append(user_message)
        recent_messages = dialog_history[-3:] if len(dialog_history) > 3 else dialog_history
        input_text = context + " " + " ".join(recent_messages)
    
    input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt')
    chat_response_ids = model.generate(
        input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        top_p=0.9,
        no_repeat_ngram_size=3
    )
    
    dialog_response = tokenizer.decode(chat_response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    if not dialog_history and (not dialog_response or len(dialog_response.strip()) < 10):
        from random import choice
        dialog_response = choice(initial_prompts)
    
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
    
    dialog_history.append(response)
    chat_history[session_id]['dialog_history'] = dialog_history
    
    detail_context = []
    if current_details:
        if 'gender' in current_details:
            detail_context.append(f"The suspect is {current_details['gender']}")
        if 'hair color' in current_details:
            detail_context.append(f"has {current_details['hair color']} hair")
        if 'face shape' in current_details:
            detail_context.append(f"has a {current_details['face shape']} face")
        if 'has moustache' in current_details:
            has_moustache = "has" if current_details['has moustache'].lower() == 'yes' else "doesn't have"
            detail_context.append(f"{has_moustache} a moustache")
    
    if detail_context:
        chat_history[session_id]['context'] = context + " " + ", ".join(detail_context) + "."

    return jsonify({'response': response})