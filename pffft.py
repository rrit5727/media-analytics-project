import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

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
    'page': 1,  # Page number (start with 1),
    
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
                description = article.get('description', '') or ''
                content = article.get('content', '') or ''
                published_at = article.get('publishedAt', '')  # Get the published date

                # Use description or content if available, or fallback to empty string
                body = description or content

                # Parse HTML content to extract plain text (if needed)
                soup = BeautifulSoup(body, 'html.parser')
                full_text = soup.get_text()

                # Create a dictionary for each article
                article_dict = {
                    'headline': headline,
                    'full_text': full_text,
                    'published_at': published_at  # Include published date in the dictionary
                }

                # Append dictionary to articles list
                articles_list.append(article_dict)

        else:
            pass  # Optionally handle error silently without printing

    except requests.exceptions.RequestException as e:
        pass  # Optionally handle request error silently without printing

    return articles_list

# Function to analyze headlines for vague references
def analyze_headline(headline):
    vague_references = [
        r'star', r'celebrity', r'actor', r'actress', r'singer', r'rapper',
        r'athlete', r'player', r'politician', r'leader', r'official',
        r'expert', r'professional', r'icon', r'legend', r'veteran',
        r'personality', r'figure', r'tycoon', r'mogul', r'boss',
        r'chief', r'exec', r'CEO', r'founder', r'creator', r'producer',
        r'director', r'host', r'anchor', r'journalist', r'reporter',
        r'correspondent', r'model', r'designer', r'chef', r'artist',
        r'author', r'writer', r'comedian', r'influencer', r'blogger',
        r'pioneer', r'innovator', r'visionary', r'guru', r'genius',
        r'wizard', r'mastermind', r'virtuoso', r'savant', r'protege',
        r'phenom', r'maverick', r'prodigy', r'specialist', r'expert',
        r'guru', r'hero', r'villain', 
        r'royalty', r'heir', r'heiress', r'artist', r'sculptor', r'painter',
        r'composer', r'conductor', r'dancer', r'performer', r'entertainer',
        r'starlet', r'visionary', r'powerhouse', r'champion', r'genius',
        r'oracle', r'authority', r'warrior', r'champion', r'pundit', r'sage',
        r'commander', r'strategist', r'mind', r'virtuoso', r'architect',
        r'explorer', r'counselor', r'wizard', r'master', r'philosopher',
        r'sage', r'elder', r'giant', 
        r'millionaire', r'billionaire', r'titan', r'captain', r'legendary',
        r'famous', r'notorious', r'illustrious', r'magnate', r'industrialist', r'musician', r'A-lister', r'nominee',
    ]

    # Constructing the regular expression directly
    pattern = r'\b(?:' + '|'.join(vague_references) + r')\b'
    
    matches = re.findall(pattern, headline.lower())
    
    if matches:
        return matches[0]
    else:
        return None

# Function to filter articles with vague references and store them in a dictionary
def filter_articles_with_vague_references(articles):
    refined_articles_dict = {}

    for index, article in enumerate(articles):
        headline = article['headline']
        full_text = article['full_text']
        
        match = analyze_headline(headline)
        if match:
            # Store article in the dictionary
            refined_articles_dict[index] = {
                'headline': headline,
                'full_text': full_text,
                'match': match  # Include the matched vague reference for debugging
            }
        else:
            pass  # Optionally handle articles without vague references

    return refined_articles_dict

# If this file is executed directly, fetch articles, filter for vague references, and print the headlines of refined articles
if __name__ == "__main__":
    articles = fetch_articles()
    if articles:
        refined_articles_dict = filter_articles_with_vague_references(articles)
        
        # Print only the headlines of refined articles
        print("Refined Article Headlines:")
        for index, article_data in refined_articles_dict.items():
            print(f"Article {index + 1}: {article_data['headline']}")

    else:
        print("No articles fetched")