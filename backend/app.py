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
    
    extracted_details = extract_details(user_message)
    missing_details = [detail for detail in required_details if detail not in extracted_details]
    
    if missing_details:
        response = f"Please provide more details about: {', '.join(missing_details)}"
    else:
        rephrased_details = rephrase_details(extracted_details)
        image_url = generate_image_with_dalle(rephrased_details)
        response = f"Is this similar to your suspect: {image_url}"
    
    return jsonify({'response': response})