from flask import Flask, render_template, request, jsonify, url_for, redirect
import pandas as pd
import openai
import os
import time
import threading
import PyPDF2
from werkzeug.utils import secure_filename
from generate_images import process_pdf
from src.file_service import update_dataset  # Import the new script

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'pdf_folder'
app.config['STATIC_FOLDER'] = 'static'

# Load the dataset
dataset = pd.read_csv('lab_results.csv')

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Rate limiting variables
rate_limit_interval = 5  # Reduced interval to improve response rate
daily_request_count = 0
max_daily_requests = 200
daily_token_count = 0
max_daily_tokens = 200000
start_of_day = time.time()
lock = threading.Lock()
last_request_time = time.time()  # Initialize last_request_time

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

@app.route('/')
def home():
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    # Load data for dashboard
    data = [
        {"Test": "WBC", "Value": 6.13, "Image": "WBC.png"},
        {"Test": "RBC", "Value": 4.86, "Image": "RBC.png"},
        {"Test": "HGB", "Value": 13.3, "Image": "HGB.png"},
        {"Test": "HCT", "Value": 41.0, "Image": "HCT.png"},
        {"Test": "MCV", "Value": 84.4, "Image": "MCV.png"},
        {"Test": "MCH", "Value": 27.4, "Image": "MCH.png"},
        {"Test": "MCHC", "Value": 32.4, "Image": "MCHC.png"},
        {"Test": "RDW", "Value": 13.7, "Image": "RDW.png"},
        {"Test": "PLATELET COUNT", "Value": 227, "Image": "PLATELET_COUNT.png"},
        {"Test": "Hemoglobin A1c", "Value": 5.2, "Image": "Hemoglobin_A1c.png"},
        {"Test": "Glucose", "Value": 99, "Image": "Glucose.png"}
    ]
    return render_template('dashboard.html', data=data)


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        output_folder = app.config['STATIC_FOLDER']
        image_paths = process_pdf(file_path, output_folder)
        return jsonify({"message": "File successfully uploaded and processed", "images": image_paths}), 200

@app.route('/chat', methods=['POST'])
def chat():
    global daily_request_count, daily_token_count, last_request_time

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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
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
            print(f"Error: {e}")
            return jsonify({'reply': 'There was an error processing your request. Please try again later.'}), 500

        daily_request_count += 1
        daily_token_count += tokens_used

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)
