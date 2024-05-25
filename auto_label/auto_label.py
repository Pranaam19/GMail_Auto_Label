import gmail_api as gmail
import ai_utils as ai
import json
import csv

# Load API key from .env file
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("PALM_API_KEY")

def extract_user_info(json_file_path='user_info.json'):
    # Read data from JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract information
    user_info = data.get('user_info', '')
    label_mapping = data.get('label_mapping', {})
    max_results = data.get('max_results', 15)

    return user_info, label_mapping, max_results