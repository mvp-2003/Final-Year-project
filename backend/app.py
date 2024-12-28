from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist')

@app.route('/')
def frontpage_index():
    return send_from_directory(app.template_folder, 'index.html')