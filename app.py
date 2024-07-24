from flask import Flask, request, jsonify, send_file
import pandas as pd
import openai
import os
import time
import threading
import PyPDF2
from werkzeug.utils import secure_filename
import matplotlib
import matplotlib.pyplot as plt
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Use 'Agg' backend for Matplotlib to avoid threading issues
matplotlib.use('Agg')

# Flask app initialization
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'pdf_folder'
app.config['STATIC_FOLDER'] = 'static'

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['STATIC_FOLDER'], exist_ok=True)

# Load the dataset
dataset = pd.read_csv('lab_results.csv')

# Set OpenAI API key
openai.api_key = "insert-api-key"

# Global variables for rate limiting and extracted text
rate_limit_interval = 5  # Reduced interval to improve response rate
daily_request_count = 0
max_daily_requests = 200
daily_token_count = 0
max_daily_tokens = 200000
start_of_day = time.time()
lock = threading.Lock()
last_request_time = time.time()  # Initialize last_request_time
extracted_text_global = ""

# Function to reset daily counters
def reset_daily_counters():
    global daily_request_count, daily_token_count, start_of_day
    while True:
        time.sleep(86400)  # Sleep for one day
        with lock:
            daily_request_count = 0
            daily_token_count = 0
            start_of_day = time.time()

# Start a thread to reset the daily counters
threading.Thread(target=reset_daily_counters, daemon=True).start()

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def parse_pdf_text(text):
    data = {}
    lines = text.split("\n")
    
    for line in lines:
        if "WBC" in line and "x10(3)" in line:
            data["WBC"] = float(line.split()[1])
        elif "RBC" in line and "x10(6)" in line:
            data["RBC"] = float(line.split()[1])
        elif "HGB" in line and "g/dL" in line:
            data["HGB"] = float(line.split()[1])
        elif "HCT" in line and "%" in line:
            data["HCT"] = float(line.split()[1])
        elif "MCV" in line and "fL" in line:
            data["MCV"] = float(line.split()[1])
        elif "MCH" in line and "pg" in line:
            data["MCH"] = float(line.split()[1])
        elif "MCHC" in line and "g/dL" in line:
            data["MCHC"] = float(line.split()[1])
        elif "RDW" in line and "%" in line:
            data["RDW"] = float(line.split()[1])
        elif "PLATELET COUNT" in line and "x10(3)/uL" in line:
            try:
                data["PLATELET COUNT"] = float(line.split()[2])
            except ValueError:
                data["PLATELET COUNT"] = float(line.split()[3])
        elif "Hemoglobin A1c" in line and "%" in line:
            data["Hemoglobin A1c"] = float(line.split()[2])
        elif "Glucose" in line and "mg/dL" in line:
            data["Glucose"] = float(line.split()[1])
    return data

def visualize_lab_results(data):
    num_tests = len(data)
    cols = 2
    rows = (num_tests // cols) + (num_tests % cols > 0)
    fig, ax = plt.subplots(rows, cols, figsize=(6, 3))  # Adjusted the figure size
    fig.tight_layout(pad=5.0)
    
    reference_ranges = {
        "WBC": (4.0, 10.1),
        "RBC": (3.58, 5.19),
        "HGB": (11.0, 15.5),
        "HCT": (31.5, 44.8),
        "MCV": (78.0, 98.0),
        "MCH": (25.2, 32.6),
        "MCHC": (31.0, 34.7),
        "RDW": (12.0, 15.5),
        "PLATELET COUNT": (140, 425),
        "Hemoglobin A1c": (0.0, 5.7),
        "Glucose": (70, 99)
    }

    ax = ax.flatten()
    for i, (test, value) in enumerate(data.items()):
        ref_range = reference_ranges[test]
        all_range = [ref_range[0] - 10, ref_range[1] + 10]  # Adjust the overall range for visualization
        
        ax[i].hlines(0, all_range[0], all_range[1], color='lightgray', linewidth=8)
        ax[i].hlines(0, ref_range[0], ref_range[1], color='lightgreen', linewidth=8)
        ax[i].plot([value], [0], 'ks', markersize=12)  # Black square for the specific value
        
        ax[i].set_xlim(all_range[0], all_range[1])
        ax[i].set_yticks([])
        ax[i].set_title(f'{test}', fontsize=14, pad=20)
        
        ax[i].annotate(f'{value}', xy=(value, 0), xytext=(0, -30), textcoords='offset points',
                       bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'),
                       ha='center', fontsize=12)
        ax[i].annotate(f'{ref_range[0]}', xy=(ref_range[0], 0), xytext=(0, 10), textcoords='offset points',
                       ha='center', fontsize=10, color='gray')
        ax[i].annotate(f'{ref_range[1]}', xy=(ref_range[1], 0), xytext=(0, 10), textcoords='offset points',
                       ha='center', fontsize=10, color='gray')
    
    for j in range(i + 1, len(ax)):
        fig.delaxes(ax[j])  # Remove unused subplots
    
    plot_path = os.path.join(app.config['STATIC_FOLDER'], 'lab_results_number_line.png')
    plt.savefig(plot_path)
    plt.close()
    return plot_path

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health Data Chatbox</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                width: 400px;
                max-width: 100%;
                padding: 20px;
                box-sizing: border-box;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .chatbox {
                width: 100%;
                height: 300px;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                overflow-y: scroll;
                background-color: #f9f9f9;
            }
            .input-group {
                display: flex;
                margin-top: 10px;
            }
            .input {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }
            .button {
                padding: 10px 20px;
                background: #007BFF;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                margin-left: 10px;
            }
            .button:hover {
                background: #0056b3;
            }
            .message {
                margin: 5px 0;
                padding: 10px;
                border-radius: 4px;
            }
            .message.user {
                background-color: #007BFF;
                color: white;
                text-align: right;
            }
            .message.bot {
                background-color: #e1e1e1;
                color: #333;
            }
            .upload-group {
                margin-top: 20px;
                text-align: center;
            }
            #uploadResult {
                margin-top: 10px;
                text-align: center;
                color: #007BFF;
            }
            .visualization img {
                max-width: 100%;
                height: auto;
                display: block;
                margin: 0 auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Health Data Chatbox</h1>
            <div class="chatbox" id="chatbox"></div>
            <div class="input-group">
                <input type="text" class="input" id="message" placeholder="Type your message here">
                <button class="button" onclick="sendMessage()">Send</button>
            </div>
            <div class="upload-group">
                <form id="uploadForm" action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" id="file">
                    <button type="button" class="button" onclick="uploadPDF()">Upload PDF</button>
                </form>
                <div id="uploadResult"></div>
            </div>
        </div>
        <script>
            function sendMessage() {
                var message = document.getElementById('message').value;
                var chatbox = document.getElementById('chatbox');
                
                var userMessage = document.createElement('div');
                userMessage.className = 'message user';
                userMessage.textContent = 'You: ' + message;
                chatbox.appendChild(userMessage);

                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({message: message}),
                })
                .then(response => response.json())
                .then(data => {
                    var botMessage = document.createElement('div');
                    botMessage.className = 'message bot';
                    simulateTyping(botMessage, 'Bot: ' + data.reply, chatbox);

                    if (data.visualization) {
                        var botImageMessage = document.createElement('div');
                        botImageMessage.className = 'message bot';
                        var img = document.createElement('img');
                        img.src = data.visualization;
                        img.alt = 'Lab Results Visualization';
                        img.classList.add('visualization');  // Add class for styling
                        botImageMessage.appendChild(img);
                        chatbox.appendChild(botImageMessage);
                    }
                });

                document.getElementById('message').value = '';
            }

            function uploadPDF() {
                var form = document.getElementById('uploadForm');
                var formData = new FormData(form);

                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    var uploadResult = document.getElementById('uploadResult');
                    uploadResult.textContent = data.message;
                })
                .catch(error => {
                    var uploadResult = document.getElementById('uploadResult');
                    uploadResult.textContent = 'Error uploading file.';
                });
            }

            function simulateTyping(element, text, chatbox) {
                element.textContent = '';
                chatbox.appendChild(element);
                chatbox.scrollTop = chatbox.scrollHeight;

                let i = 0;
                const interval = setInterval(() => {
                    if (i < text.length) {
                        element.textContent += text.charAt(i);
                        chatbox.scrollTop = chatbox.scrollHeight;
                        i++;
                    } else {
                        clearInterval(interval);
                    }
                }, 30); // Adjust typing speed here (30ms per character for faster typing)
            }
        </script>
    </body>
    </html>
    '''

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
def chat():
    global daily_request_count, daily_token_count, last_request_time, extracted_text_global

    current_time = time.time()

    with lock:
        if daily_request_count >= max_daily_requests:
            return jsonify({'reply': 'Daily request limit exceeded. Please try again tomorrow.'}), 429

        if daily_token_count >= max_daily_tokens:
            return jsonify({'reply': 'Daily token limit exceeded. Please try again tomorrow.'}), 429

        if current_time - last_request_time < rate_limit_interval:
            time.sleep(rate_limit_interval - (current_time - last_request_time))

        last_request_time = current_time

        user_message = request.json['message']
        print(f"Received message: {user_message}")  # Debugging statement
        try:
            if "visualize my lab results" in user_message.lower():
                # Generate the visualization
                plot_path = visualize_lab_results(parse_pdf_text(extracted_text_global))
                return jsonify({'reply': 'Here is the visualization of your lab results:', 'visualization': f"/{plot_path}"}), 200
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant with access to health records."},
                    {"role": "user", "content": f"Here is the extracted text from the PDF:\n{extracted_text_global}"},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_reply = response['choices'][0]['message']['content'].strip()
            print(f"Bot reply: {bot_reply}")  # Debugging statement

            # Calculate token usage
            tokens_used = response['usage']['total_tokens']
            print(f"Tokens used: {tokens_used}")

        except openai.error.RateLimitError:
            return jsonify({'reply': 'API rate limit exceeded. Please wait a moment and try again.'}), 429
        except Exception as e:
            logging.error(f"Error in chat endpoint: {e}")
            return jsonify({'reply': 'There was an error processing your request. Please try again later.'}), 500

        daily_request_count += 1
        daily_token_count += tokens_used 

    return jsonify({'reply': bot_reply}) #test

if __name__ == '__main__':
    app.run(debug=True)


