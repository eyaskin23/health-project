import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY

def generate_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content'].strip()
