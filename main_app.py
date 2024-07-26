from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import openai
import os
import time
import threading
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from generate_images import process_pdf
from src.file_service import update_dataset

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['UPLOAD_FOLDER'] = 'pdf_folder'
app.config['STATIC_FOLDER'] = 'static'

# Load the dataset
dataset = pd.read_csv('lab_results.csv')

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Rate limiting variables
rate_limit_interval = 5
daily_request_count = 0
max_daily_requests = 200
daily_token_count = 0
max_daily_tokens = 200000
start_of_day = time.time()
lock = threading.Lock()
last_request_time = time.time()

def reset_daily_counters():
    global daily_request_count, daily_token_count, start_of_day
    while True:
        time.sleep(86400)
        with lock:
            daily_request_count = 0
            daily_token_count = 0
            start_of_day = time.time()

threading.Thread(target=reset_daily_counters, daemon=True).start()

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message='Invalid credentials')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            return render_template('register.html', message='Username already exists')
        finally:
            conn.close()
        
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/')
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
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
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/chatbot')
def chatbot():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
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
    if 'logged_in' not in session:
        return redirect(url_for('login'))

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
        print(f"Received message: {user_message}")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_reply = response['choices'][0]['message']['content'].strip()
            print(f"Bot reply: {bot_reply}")

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
