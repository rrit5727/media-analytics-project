from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

# Function to predict sentiment for a chunk of text
def predict_sentiment(text):
    inputs = tokenizer.encode_plus(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    return predicted_class, probabilities

# Function to handle long texts by splitting into chunks
def predict_sentiment_long_text(text, chunk_size=512):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]

    all_probabilities = []
    sentiment_labels = {0: 'very negative', 1: 'negative', 2: 'neutral', 3: 'positive', 4: 'very positive'}
    
    for i, chunk in enumerate(chunks):
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        predicted_class, probabilities = predict_sentiment(chunk_text)
        all_probabilities.append(probabilities)
        sentiment = sentiment_labels[predicted_class]
        print(f"Chunk [{i * chunk_size}:{(i + 1) * chunk_size}] - Predicted sentiment: {sentiment}")
        print(f"Chunk [{i * chunk_size}:{(i + 1) * chunk_size}] - Probabilities: {probabilities}")

    avg_probabilities = torch.mean(torch.cat(all_probabilities), dim=0)
    overall_predicted_class = torch.argmax(avg_probabilities, dim=0).item()
    overall_sentiment = sentiment_labels[overall_predicted_class]
    
    return overall_predicted_class, avg_probabilities, overall_sentiment

# Example text for sentiment analysis
text = """

July 1, 2024 — A major retail chain's recent introduction of advanced technological innovations has sparked controversy and concern among stakeholders, raising questions about its impact on traditional operations and workforce.

The chain's rollout of AI-powered systems, including automated customer service, inventory management, and checkout processes, has encountered significant backlash.

Automated Customer Service Systems

Critics argue that the deployment of automated customer service systems threatens to depersonalize interactions with customers, potentially reducing the quality of service and eliminating jobs traditionally held by human staff.

AI-Powered Inventory Management

The implementation of AI-powered inventory management systems has also come under scrutiny, with concerns about job displacement and the reliance on algorithms to dictate stock levels, potentially overlooking nuanced factors that human oversight provides.

Enhanced Checkout Processes

While touted for convenience, the introduction of self-service checkout stations and mobile payment options has drawn criticism for its potential to marginalize consumers less familiar with technology and to diminish opportunities for personal interaction within retail settings.

Public Backlash

Public reaction has been largely critical, with consumers expressing skepticism about the chain's commitment to maintaining human-centered service and ethical employment practices amidst the rapid adoption of automation.

Labor Concerns

Trade unions and worker advocacy groups have voiced strong opposition, highlighting fears of job loss and the erosion of job security in an already precarious economic climate.

Future Implications

The future implications of these technological changes remain uncertain, with ongoing debates surrounding their potential long-term effects on both the retail workforce and customer experience.

Conclusion

The retail chain's technological overhaul, while aimed at enhancing operational efficiency, has ignited a contentious debate about the ethical and societal implications of accelerating automation in retail environments. As stakeholders continue to voice concerns, the chain faces a critical juncture in balancing innovation with maintaining trust and transparency with its customers and workforce alike.

"""

# Get sentiment prediction for the long text
overall_predicted_class, avg_probabilities, overall_sentiment = predict_sentiment_long_text(text)

# Print the overall results
print(f"\nOverall predicted sentiment: {overall_sentiment}")
print(f"Overall probabilities: {avg_probabilities}")