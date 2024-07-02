from pygooglenews import GoogleNews
import requests
from bs4 import BeautifulSoup

gn = GoogleNews(country='AU')

def fetch_full_article(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        article_text = ""
        # Adjust this based on the specific structure of the website
        # Here's a generic example of finding article content in a div
        article_body = soup.find('div', class_='article-body')  # Adjust based on actual structure
        if article_body:
            paragraphs = article_body.find_all('p')
            for paragraph in paragraphs:
                article_text += paragraph.text.strip() + "\n"
        return article_text
    except Exception as e:
        print(f"Error fetching article: {e}")
        return ""

def get_articles(search):
    articles = []
    search_results = gn.search(search)
    news_items = search_results['entries']
    
    for item in news_items[:2]:  # Limit to the first 10 articles
        article = {
            'title': item.title,
            'link': item.link,
            'content': fetch_full_article(item.link)  # Fetch full article content here
        }
        articles.append(article)
    
    return articles

search_term = 'football'
articles = get_articles(search_term)

# Print out the first 10 articles
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Link: {article['link']}")
    print(f"Content:\n{article['content']}")
    print("\n")