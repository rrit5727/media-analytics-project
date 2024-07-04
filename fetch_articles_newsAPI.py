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
    'pageSize': 100,  # Number of articles per page (adjust as needed)
    'page': 1,  # Page number (start with 1)
}

# Function to fetch articles
def fetch_articles():
    articles_list = []

    try:
        # Making the request
        response = requests.get(base_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # Process the data here
            for article in data.get('articles', []):
                headline = article.get('title', '')

                # Create a dictionary for each article
                article_dict = {
                    'headline': headline
                }

                # Append dictionary to articles list
                articles_list.append(article_dict)

        else:
            pass  # Optionally handle error silently without printing

    except requests.exceptions.RequestException as e:
        pass  # Optionally handle request error silently without printing

    return articles_list

# If this file is executed directly, fetch articles and print the index and headline
if __name__ == "__main__":
    articles = fetch_articles()

    # Print the index and headline of each article
    if articles:
        for index, article in enumerate(articles):
            print(f"{index + 1}: {article['headline']}")
    else:
        print("No articles fetched")