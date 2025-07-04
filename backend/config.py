import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
config = {
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'OPENAI_BASE_URL': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
    'MODEL_NAME': os.getenv('MODEL_NAME', 'gpt-3.5-turbo'),
    'MAX_TOKENS': int(os.getenv('MAX_TOKENS', 1000)),
    'TEMPERATURE': float(os.getenv('TEMPERATURE', 0.7)),
    'DATA_PATH': os.getenv('DATA_PATH', 'data/products.json')
}