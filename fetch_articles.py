import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variables
api_key = os.getenv('NEWS_API_KEY')

# Base URL for News API everything endpoint
base_url = 'https://newsapi.org/v2/everything'

# Parameters for the API request
params = {
    'apiKey': api_key,
    'sources': 'news-com-au',  # Specify news.com.au as the source
    'pageSize': 1,  # Number of articles per page (fetch only 1 article)
    'page': 1,  # Page number (start with 1)
}

# Function to fetch articles
def fetch_articles():
    article_dict = {}

    try:
        # Making the request
        response = requests.get(base_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # Process the data here
            if data.get('articles'):
                article = data['articles'][0]  # Get the first article
                article_dict = {
                    'headline': article.get('title', ''),
                    'content': article.get('content', ''),
                    'published_at': article.get('publishedAt', ''),
                    'source_name': article['source']['name'],
                    'url': article['url'],
                    'image_url': article['urlToImage']
                }

        else:
            pass  # Optionally handle error silently without printing

    except requests.exceptions.RequestException as e:
        pass  # Optionally handle request error silently without printing

    return article_dict

# If this file is executed directly, fetch the first article and print the whole response object
if __name__ == "__main__":
    article = fetch_articles()

    # Print the whole response object for the first article
    if article:
        print("Response Object for the First Article:")
        print(article)
    else:
        print("No articles fetched")