from fetch_articles import fetch_articles

if __name__ == "__main__":
    articles = fetch_articles()

    # Print the headlines of fetched articles
    if articles:
        print("Articles Imported:")
        for index, article in enumerate(articles):
            print(f"Headline {index + 1}: {article['headline']}")
            print()  # Add a newline for clarity between articles
    else:
        print("No articles fetched")