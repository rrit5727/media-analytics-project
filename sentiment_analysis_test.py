import torch
from transformers import BertForSequenceClassification, BertTokenizer
import spacy
from collections import Counter

# Load tokenizer and model for sentiment analysis
tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')

# Load spaCy for NER
nlp = spacy.load('en_core_web_sm')

# Sentiment labels
sentiment_labels = {
    0: 'positive',
    1: 'negative',
    2: 'neutral'
}

# Function to chunk input_ids and attention_mask
def get_input_ids_and_attention_mask_chunk(tokens, chunksize=510):
    input_ids = tokens['input_ids'][0]
    attention_mask = tokens['attention_mask'][0]

    input_id_chunks = []
    attention_mask_chunks = []

    for i in range(0, len(input_ids), chunksize):
        input_chunk = input_ids[i:i + chunksize]
        attention_chunk = attention_mask[i:i + chunksize]

        # Add [CLS] and [SEP] tokens at the beginning and end of each chunk
        input_chunk = torch.cat([torch.tensor([101]), input_chunk, torch.tensor([102])])
        attention_chunk = torch.cat([torch.tensor([1]), attention_chunk, torch.tensor([1])])

        # Pad if necessary
        padding_length = chunksize + 2 - input_chunk.shape[0]
        if padding_length > 0:
            input_chunk = torch.cat([input_chunk, torch.zeros(padding_length)])
            attention_chunk = torch.cat([attention_chunk, torch.zeros(padding_length)])

        input_id_chunks.append(input_chunk.unsqueeze(0))
        attention_mask_chunks.append(attention_chunk.unsqueeze(0))

    return input_id_chunks, attention_mask_chunks

# List to store results
results = []

# Manually input articles as plain text
manual_articles = [
    """
Description: Iconic ’90s actress Neve Campbell has been spotted enjoying the sun in Italy ahead of her return to the Scream franchise.
Content: Iconic ’90s actress Neve Campbell has been spotted enjoying the sun in Italy ahead of her return to the Scream franchise. 
Campbell, best known for starring as Sidney Prescott in the iconic horror s
    """
]

for text in manual_articles:
    # Tokenize the text
    tokens = tokenizer.encode_plus(text, add_special_tokens=False, return_tensors='pt')

    # Get input_ids and attention_mask chunks
    input_id_chunks, attention_mask_chunks = get_input_ids_and_attention_mask_chunk(tokens)

    # Perform inference for each chunk and accumulate results
    total_probabilities = None
    chunk_sentiments = []
    chunk_probabilities = []

    for idx, (input_ids_chunk, attention_mask_chunk) in enumerate(zip(input_id_chunks, attention_mask_chunks)):
        # Prepare input dictionary
        input_dict = {
            'input_ids': input_ids_chunk.long(),
            'attention_mask': attention_mask_chunk.int()
        }

        # Perform inference
        outputs = model(**input_dict)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=-1)

        # Predict sentiment for the chunk
        predicted_sentiment = torch.argmax(probabilities).item()
        chunk_sentiments.append(predicted_sentiment)
        chunk_probabilities.append(probabilities.tolist())

        # Accumulate probabilities for mean calculation
        if total_probabilities is None:
            total_probabilities = probabilities
        else:
            total_probabilities += probabilities

    # Calculate mean probabilities
    mean_probabilities = total_probabilities / len(input_id_chunks)

    # Predicted sentiment for the entire text is the argmax of mean probabilities
    predicted_sentiment = torch.argmax(mean_probabilities).item()

    # Overall predicted sentiment
    overall_sentiment_label = sentiment_labels[predicted_sentiment]

    # Extract entities from the text
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PERSON', 'GPE']]

    # Count occurrences of each entity
    entity_counts = Counter(entities)
    most_common_entities = entity_counts.most_common(2)

    # Create results dictionary
    result_dict = {
        'text': text[:50] + "...",  # Show the first 50 characters of the text for reference
        'overall_sentiment': overall_sentiment_label,
        'most_common_entities': most_common_entities,
        'chunk_sentiments': chunk_sentiments,
        'chunk_probabilities': chunk_probabilities,
        'mean_probabilities': mean_probabilities.tolist()
    }

    # Append results dictionary to results list
    results.append(result_dict)

# Print the results
for result in results:
    print(f"Text: {result['text']}")
    print(f"Overall Sentiment: {result['overall_sentiment']}")
    print(f"Most Common Entities: {result['most_common_entities']}")
    print("Chunk Sentiments and Probabilities:")
    for idx, (sentiment, probabilities) in enumerate(zip(result['chunk_sentiments'], result['chunk_probabilities'])):
        print(f"  Chunk {idx + 1}: Sentiment: {sentiment_labels[sentiment]}")
        print(f"    Probabilities: {probabilities}")
    print(f"Mean Probabilities: {result['mean_probabilities']}")
    print("---------------------------")