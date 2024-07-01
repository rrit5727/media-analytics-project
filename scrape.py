import requests
from bs4 import BeautifulSoup

def fetch_article_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <div> elements with specific styling attributes
    div_elements = soup.find_all('div', style="color:rgb(64, 68, 70);font-family:sans-serif;font-size:18px;")
    
    # Extract text content from selected <div> elements
    for div in div_elements:
        article_text = div.get_text()
        print(article_text)

if __name__ == "__main__":
    url = 'https://archive.is/nJq9Z'  # Replace with your actual URL
    
    print(f"Fetching article from {url}...")
    fetch_article_content(url)