import io
import logging
import PyPDF2
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from matplotlib import pyplot as plt
import pandas as pd
import openai
import os
import time
import threading
import sqlite3
import csv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from generate_images import process_pdf
from src.file_service import update_dataset
from generate_plots import generate_plots

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'pdf_folder'
app.config['STATIC_FOLDER'] = 'static'
app.secret_key = os.urandom(24)

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

extracted_text_global = ""


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
        return redirect(url_for('index'))
    return redirect('/index')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    data = [
        {"Test": "WBC", "Value": 6.13, "Image": "WBC.svg"},
        {"Test": "RBC", "Value": 4.86, "Image": "RBC.svg"},
        {"Test": "HGB", "Value": 13.3, "Image": "HGB.svg"},
        {"Test": "HCT", "Value": 41.0, "Image": "HCT.svg"},
        {"Test": "MCV", "Value": 84.4, "Image": "MCV.svg"},
        {"Test": "MCH", "Value": 27.4, "Image": "MCH.svg"},
        {"Test": "MCHC", "Value": 32.4, "Image": "MCHC.svg"},
        {"Test": "RDW", "Value": 13.7, "Image": "RDW.svg"},
        {"Test": "PLATELET_COUNT", "Value": 227, "Image": "PLATELET_COUNT.svg"},
        {"Test": "Hemoglobin_A1c", "Value": 5.2, "Image": "Hemoglobin_A1c.svg"},
        {"Test": "Glucose", "Value": 99, "Image": "Glucose.svg"},
        #{"Test": "Smoking Rates vs Air Quality", "Value": "Fresno: ", "Image": "california.svg"},
        #{"Test": "Air Quality", "Value": "Fresno: ", "Image": "fresno_aqi.svg"},
        #{"Test": "State Population", "Value": "2022", "Image": "california_population.svg"}

    ]
    return render_template('dashboard.html', data=data)

@app.route('/profile')
def profile():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

@app.route('/data_input')
def data_input():
    return render_template('data_input.html')

def plot_to_svg(data, test):
    plt.figure()
    plt.plot(range(len(data)), data, marker='o', linestyle='-', color='b')
    plt.title(test)
    plt.xlabel('Time')
    plt.ylabel('Value')
    img = io.BytesIO()
    plt.savefig(img, format='svg')
    img.seek(0)
    svg_data = img.getvalue().decode()
    plt.close()
    return svg_data

@app.route('/social_determinants')
def social_determinants():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    # Dummy data for visualization
    social_data = [
        {"Test": "Fresno Air Quality", "Value": 75, "Image": "fresno_aqi.svg"},
        {"Test": "California Population", "Value": 38866193, "Image": "california_population.svg"},
        {"Test": "Fresno Unemployment", "Value": 3.8, "Image": "fresno_unemployment.svg"}
    ]
    
    return render_template('social_determinants.html', data=social_data)


@app.route('/index')
def index():
    
    return render_template('index.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    name = request.form['name']
    address = request.form['address']
    age = request.form['age']
    gender = request.form['gender']

    file_exists = os.path.isfile('user_data.csv')
    
    with open('user_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Name', 'Address', 'Age', 'Gender'])
        writer.writerow([name, address, age, gender])

    return redirect(url_for('profile'))


@app.route('/generate_plots')
def generate_plots():
    # Example time-series data
    time_series_data = {
        "WBC": [6.1, 6.3, 6.2, 6.4, 6.1],
        "RBC": [4.7, 4.8, 4.9, 4.8, 4.9],
        "HGB": [13.2, 13.3, 13.5, 13.4, 13.3],
        "HCT": [40.0, 41.0, 42.0, 41.0, 40.5],
        "MCV": [85.0, 84.5, 84.0, 83.5, 84.0],
        "MCH": [28.0, 27.5, 27.0, 26.5, 27.0],
        "MCHC": [33.0, 32.5, 32.0, 32.5, 32.0],
        "RDW": [13.5, 13.6, 13.7, 13.8, 13.7],
        "PLATELET COUNT": [220, 230, 240, 235, 225],
        "Hemoglobin A1c": [5.5, 5.4, 5.3, 5.4, 5.5],
        "Glucose": [100, 98, 95, 97, 96]
    }
    svg_plots = {}
    for test, values in time_series_data.items():
        svg_plots[test] = plot_to_svg(values, test)
    return jsonify(svg_plots)

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
        generate_plots()
        return jsonify({"message": "File successfully uploaded and processed"}), 200

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

    return jsonify({'reply': bot_reply})

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    data = request.json.get('data')
    
    if data:
        try:
            # Prepare the prompt with the given data
            prompt = "Generate a summary for the follow health data. Please keep it concise, max three/four sentences.:\n\n"
            for stat in data:
                prompt += f"{stat['Test']}: {stat['Value']}\n"

            # Generate the summary using OpenAI's GPT-3.5 turbo
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )

            summary = response.choices[0].message['content'].strip()
        except Exception as e:
            summary = f"Error generating summary: {str(e)}"
    else:
        summary = "No data provided."

    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True, port = 7000)

