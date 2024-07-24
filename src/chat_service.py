import time
import openai
import threading
from flask import request, jsonify
from config import Config
from src.openai_service import generate_response
import logging

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

threading.Thread(target=reset_daily_counters, daemon=True).start()

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
