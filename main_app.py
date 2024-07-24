from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from src.chat_service import chat
from utils.pdf_utils import extract_text_from_pdf, parse_pdf_text
from src.file_service import update_dataset
from utils.plot_utils import visualize_lab_results
from config import Config
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

dataset = pd.read_csv('lab_results.csv')
extracted_text_global = ""

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/results', methods=['GET'])
def get_results():
    results = dataset.to_dict(orient='records')
    return jsonify(results)

@app.route('/results/<test_name>', methods=['GET'])
def get_result_by_test(test_name):
    filtered_results = dataset[dataset['Test'].str.contains(test_name, case=False)]
    if filtered_results.empty:
        return jsonify({"message": "Test not found"}), 404
    results = filtered_results.to_dict(orient='records')
    return jsonify(results)

@app.route('/upload', methods=['POST'])
def upload_file():
    global extracted_text_global
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        extracted_text_global = extract_text_from_pdf(file_path)
        parsed_data = parse_pdf_text(extracted_text_global)
        update_dataset(parsed_data)
        return jsonify({"message": "File successfully uploaded and processed"}), 200

@app.route('/visualize', methods=['GET'])
def visualize():
    data = dataset.to_dict(orient='records')
    plot_path = visualize_lab_results(parse_pdf_text(extracted_text_global))
    if plot_path:
        return send_file(plot_path, mimetype='image/png')
    else:
        return jsonify({"message": "Error creating visualization"}), 500

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    return chat()

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
