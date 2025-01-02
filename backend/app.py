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
            'dialog_history': []
        }
    
    new_details = extract_details(user_message)
    current_details = chat_history[session_id]['details']
    
    current_details.update(new_details)
    chat_history[session_id]['details'] = current_details
    
    structured_response = generate_response(current_details, user_message)
    
    if "I need some more information" in structured_response:
        response = structured_response
    else:
        dialog_history = chat_history[session_id]['dialog_history']
        dialog_history.append(user_message)
        
        full_context = " ".join(dialog_history[-3:])
        
        input_ids = tokenizer.encode(full_context + tokenizer.eos_token, return_tensors='pt')
        chat_response_ids = model.generate(
            input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            temperature=0.7,
            top_p=0.9,
            no_repeat_ngram_size=3
        )
        
        response = tokenizer.decode(chat_response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        if not response or len(response.strip()) < 10:
            response = structured_response
            
        dialog_history.append(response)
        chat_history[session_id]['dialog_history'] = dialog_history

    return jsonify({'response': response})