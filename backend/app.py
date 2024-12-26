from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from helper import rephrase_details, generate_image_with_dalle, required_details
from detector import extract_details

app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist')

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

    input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')
    chat_history_ids = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    bot_response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

    extracted_details = extract_details(user_message)
    missing_details = [detail for detail in required_details if detail not in extracted_details]
    
    if missing_details:
        response = f"{bot_response} By the way, could you tell me more about: {', '.join(missing_details)}?"
    else:
        rephrased_details = rephrase_details(extracted_details)
        image_url = generate_image_with_dalle(rephrased_details)
        response = f"Is this similar to your suspect: {image_url}"
    
    return jsonify({'response': response})