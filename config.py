import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    UPLOAD_FOLDER = 'pdf_folder'
    STATIC_FOLDER = 'static'
    MAX_DAILY_REQUESTS = 200
    MAX_DAILY_TOKENS = 200000
    RATE_LIMIT_INTERVAL = 5  # in seconds
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
