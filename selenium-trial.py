import requests
from bs4 import BeautifulSoup


def fetch_news_articles(company_name, num_articles=5):
    url = f"https://news.google.com/search?q={company_name}&hl=en-US&gl=US&ceid=US%3Aen"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    print(f"Fetching news articles for '{company_name}'...")
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('article')
        results = []
        count = 0

        for article in articles:
            if count >= num_articles:
                break

            headline = article.find('h3', class_='ipQwMb ekueJc RD0gLb')
            if headline:
                headline_text = headline.text.strip()
                link = article.find('a')['href']
                article_text = fetch_article_text(link)  # Function to fetch full article text
                results.append({
                    'headline': headline_text,
                    'url': link,
                    'article_text': article_text
                })
                count += 1

        return results

    except Exception as e:
        print(f"Error fetching news articles: {e}")
        return []


def fetch_article_text(article_url):
    # Function to fetch full article text from the article URL using requests and BeautifulSoup
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])
        return article_text
    except Exception as e:
        print(f"Error fetching article text: {e}")
        return ""


# Example usage
if __name__ == "__main__":
    company_name = "Google"
    articles = fetch_news_articles(company_name, num_articles=5)

    if articles:
        for idx, article in enumerate(articles, start=1):
            print(f"Article {idx}: {article['headline']}")
            print(f"URL: {article['url']}")
            print(f"Article Text: {article['article_text'][:300]}...")  # Print first 300 characters for brevity
            print("-" * 50)
    else:
        print(f"No articles found for '{company_name}'")