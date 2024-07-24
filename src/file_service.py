from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import pandas as pd
from utils.pdf_utils import extract_text_from_pdf, parse_pdf_text
from utils.plot_utils import visualize_lab_results
from config import Config


dataset = pd.read_csv('lab_results.csv')

def update_dataset(parsed_data):
    global dataset
    new_data = pd.DataFrame([parsed_data])
    dataset = pd.concat([dataset, new_data], ignore_index=True)
    dataset.to_csv('lab_results.csv', index=False)

def get_results():
    results = dataset.to_dict(orient='records')
    return jsonify(results)

def get_result_by_test(test_name):
    filtered_results = dataset[dataset['Test'].str.contains(test_name, case=False)]
    if filtered_results.empty:
        return jsonify({"message": "Test not found"}), 404
    results = filtered_results.to_dict(orient='records')
    return jsonify(results)

def upload_file():
    global extracted_text_global
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)
        extracted_text_global = extract_text_from_pdf(file_path)
        parsed_data = parse_pdf_text(extracted_text_global)
        update_dataset(parsed_data)
        return jsonify({"message": "File successfully uploaded and processed"}), 200

def visualize():
    plot_path = os.path.join(Config.STATIC_FOLDER, 'lab_results_number_line.png')
    visualize_lab_results(parse_pdf_text(extracted_text_global), plot_path)
    if os.path.exists(plot_path):
        return send_file(plot_path, mimetype='image/png')
    else:
        return jsonify({"message": "Error creating visualization"}), 500
