from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from detector import extract_details
from logic import generate_response
from transformers import AutoModelForCausalLM, AutoTokenizer

app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist')
CORS(app)

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.route('/')
def frontpage_index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    extracted_details = extract_details(user_message)
    response = generate_response(extracted_details, user_message)

    if "Could you please provide more details" in response:
        input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')
        chat_history_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        bot_response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        response = bot_response

    return jsonify({'response': response})