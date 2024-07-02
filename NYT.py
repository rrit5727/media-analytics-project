import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
api_key = os.getenv('NYT_API_KEY')

# Base URL for the New York Times Top Stories API
base_url = 'https://api.nytimes.com/svc/topstories/v2/'

# Section of interest (e.g., 'world', 'business', 'technology', etc.)
section = 'world'

# Full endpoint URL
url = f"{base_url}{section}.json"

# Parameters for the API request
params = {
    'api-key': api_key
}

try:
    # Making the request
    response = requests.get(url, params=params)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        # Process the data here
        # Example: print out the headline, abstract, and URL of each article
        for article in data.get('results', []):
            headline = article.get('title', '')
            abstract = article.get('abstract', '')
            web_url = article.get('url', '')
            print(f"Headline: {headline}")
            print(f"Abstract: {abstract}")
            print(f"Web URL: {web_url}")
            print("---------------------------")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")