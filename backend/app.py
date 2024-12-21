from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='../frontend/dist', template_folder='../frontend/dist')

@app.route('/')
def frontpage_index():
    return send_from_directory(app.template_folder, 'index.html')