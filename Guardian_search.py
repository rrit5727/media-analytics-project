import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
api_key = os.getenv('GUARDIAN_API_KEY')

# Base URL for The Guardian API
base_url = 'https://content.guardianapis.com/search'

# Timezone conventions to exclude
exclude_timezones = ['UTC', 'GMT', 'BST', 'PDT', 'EDT', 'CET', 'AEDT', 'IST', 'JST', 'CST', 'KST', 'MSK']

# Parameters for the API request
params = {
    'q': 'NielsenIQ',  # Query term
    'api-key': api_key,
    'show-fields': 'body',  # Request to show full article body,
    'order-by': 'newest',  # Order by newest articles
}

try:
    # Making the request
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        
        # Process the data here
        for article in data.get('response', {}).get('results', []):
            headline = article.get('webTitle', '')
            body = article.get('fields', {}).get('body', '')
            
            # Exclude articles with 'GMT' in the body text or timezones in exclude_timezones
            exclude_article = any(tz in body for tz in exclude_timezones) or 'GMT' in body
            
            if not exclude_article:
                # Parse HTML content to extract plain text
                soup = BeautifulSoup(body, 'html.parser')
                full_text = soup.get_text()
                
                print(f"Headline: {headline}")
                print(f"Full Article Text:\n{full_text[:50000]}...")  # Print first 1000 characters of full text
                print("---------------------------")
            
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")