import requests
from bs4 import BeautifulSoup
import time
import re

def get_article_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    
    for article in soup.find_all('article', class_='storyblock'):
        link = article.find('a', class_='storyblock_image_link')
        title = article.find('h4')
        if link and 'href' in link.attrs and title:
            articles.append({
                'url': link['href'],
                'title': title.text.strip()
            })
    
    return articles

def get_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    full_text = ' '.join([p.text for p in paragraphs])
    return full_text[:512] + '...' if len(full_text) > 512 else full_text

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

def filter_articles_with_vague_references(articles):
    refined_articles = []

    for article in articles:
        headline = article['title']
        full_text = article['first_512_chars']
        
        match = analyze_headline(headline)
        if match:
            refined_articles.append({
                'headline': headline,
                'full_text': full_text,
                'match': match
            })
    
    return refined_articles

def scrape_articles():
    base_url = 'https://www.news.com.au/entertainment'
    article_info = get_article_info(base_url)
    articles = []

    for article in article_info[:20]:  # Limiting to first 20 articles
        try:
            # Check if the article URL contains 'video'
            if 'video' in article['url'].lower():
                print(f"Skipping video article: {article['title']} - {article['url']}")
                continue
            
            full_text = get_article_text(article['url'])
            articles.append({
                'title': article['title'],
                'first_512_chars': full_text,
                'article_url': article['url']
            })
            print(f"\nTitle: {article['title']}")
            print(f"URL: {article['url']}")
            print(f"First 512 characters: {full_text}")
            time.sleep(1)  # Be polite to the server
        except Exception as e:
            print(f"Error scraping {article['url']}: {str(e)}")

    return articles

if __name__ == "__main__":
    scraped_articles = scrape_articles()
    
    # Perform vagueness analysis on scraped articles
    refined_articles = filter_articles_with_vague_references(scraped_articles)
    
    # Print results to console
    print("\nRefined Article Headlines with Vague References:")
    for index, article_data in enumerate(refined_articles):
        print(f"Article {index + 1}:")
        print(f"Headline: {article_data['headline']}")
        print(f"Matched Vague Reference: {article_data['match']}")
        print(f"First 512 characters: {article_data['full_text']}")
        print("-" * 50)