import re
from fetch_articles import fetch_articles  # Ensure fetch_articles is correctly imported
from pprint import pprint  # for pretty printing

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
        r'guru', r'hero', r'villain', r'queen', r'king', r'prince', r'princess',
        r'royalty', r'heir', r'heiress', r'artist', r'sculptor', r'painter',
        r'composer', r'conductor', r'dancer', r'performer', r'entertainer',
        r'starlet', r'visionary', r'powerhouse', r'champion', r'genius',
        r'oracle', r'authority', r'warrior', r'champion', r'pundit', r'sage',
        r'commander', r'strategist', r'mind', r'virtuoso', r'architect',
        r'explorer', r'counselor', r'wizard', r'master', r'philosopher',
        r'sage', r'elder', r'giant', r'prince', r'princess', r'royal',
        r'millionaire', r'billionaire', r'titan', r'captain', r'legendary',
        r'famous', r'notorious', r'illustrious', r'magnate', r'industrialist', r'musician',
    ]

    pattern = r'\b(?:(?:famous|iconic|legendary|popular|well-known|renowned|celebrated|former|ex-|veteran)\s+)?(' + '|'.join(vague_references) + r')\b'
    
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
            print(f"Article filtered out: {headline}")  # Debugging output

    return refined_articles_dict

# If this file is executed directly, fetch articles, filter for vague references, and store in a dictionary
if __name__ == "__main__":
    articles = fetch_articles()
    if articles:
        # Print fetched article headlines before analysis
        print("Articles Imported Pre-Analysis:")
        for article in articles:
            print(article['headline'])
        print()  # add a blank line for clarity
        
        refined_articles_dict = filter_articles_with_vague_references(articles)
        
        # Print or use refined_articles_dict as needed
        print(f"Number of refined articles: {len(refined_articles_dict)}")
        for index, article_data in refined_articles_dict.items():
            print(f"Article {index + 1}:")
            print(f"Headline: {article_data['headline']}")
            print(f"Matched Vague Reference: {article_data['match']}")
            print(f"Full Text: {article_data['full_text']}")
            print()

        # Optionally, save refined_articles_dict to a file or import it into another module for NER analysis
    else:
        print("No articles fetched")