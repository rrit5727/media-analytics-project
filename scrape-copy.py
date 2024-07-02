import os
from dotenv import load_dotenv
import requests

# load environment variables from env file
load_dotenv()


# Access the API key
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

def fetch_top_headlines():
  url = ''