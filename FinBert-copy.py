from transformers import BertForSequenceClassification, BertTokenizer
import torch

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')

# Example text
txt = """

Major Retail Chain Explores New Technological Innovations

July 1, 2024 — A prominent retail chain is currently exploring the integration of new technological innovations across its operations, aiming to enhance efficiency and customer experience.

The initiative involves testing advanced technologies such as automated customer service systems, AI-powered inventory management, and enhanced checkout processes in select locations.

Automated Customer Service Systems

As part of the pilot program, the retail chain is deploying automated customer service systems that utilize AI algorithms to handle inquiries and provide personalized assistance to shoppers.

AI-Powered Inventory Management

Additionally, the chain is implementing AI-powered inventory management systems to optimize stock levels and streamline supply chain operations. These systems are expected to improve accuracy in forecasting demand and replenishment cycles.

Enhanced Checkout Processes

In an effort to reduce wait times and enhance convenience, the chain is rolling out enhanced checkout processes. These include self-service checkout stations and mobile payment options, providing customers with more flexible payment choices.

Future Expansion

Pending successful testing and evaluation, the retail chain plans to expand these technological innovations to more locations. Feedback from customers and operational data will inform further refinements and adjustments.

Public Response

Public reception to these innovations has been varied, with some customers expressing interest in the potential benefits of improved efficiency and convenience, while others are cautious about the impact on traditional retail jobs.

Conclusion

The retail chain's exploration of new technological innovations represents a strategic effort to modernize its operations and meet evolving consumer expectations. As the pilot program progresses, the chain aims to strike a balance between leveraging technology for operational improvements and maintaining a positive customer experience.


"""

# Tokenize the text
tokens = tokenizer.encode_plus(txt, add_special_tokens=False, return_tensors='pt')

# Function to chunk input_ids and attention_mask
def get_input_ids_and_attention_mask_chunk(tokens, chunksize=510):
    input_ids = tokens['input_ids'][0]
    attention_mask = tokens['attention_mask'][0]
    
    input_id_chunks = []
    attention_mask_chunks = []
    
    for i in range(0, len(input_ids), chunksize):
        input_chunk = input_ids[i:i+chunksize]
        attention_chunk = attention_mask[i:i+chunksize]
        
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

# Get input_ids and attention_mask chunks
input_id_chunks, attention_mask_chunks = get_input_ids_and_attention_mask_chunk(tokens)

# Sentiment labels
sentiment_labels = {
    0: 'positive',
    1: 'negative',
    2: 'neutral'
}

# Perform inference for each chunk and accumulate results
total_probabilities = None
chunk_sentiments = []

for input_ids_chunk, attention_mask_chunk in zip(input_id_chunks, attention_mask_chunks):
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
    
    # Print sentiment for the current chunk
    sentiment_label = sentiment_labels[predicted_sentiment]
    print(f"Chunk Sentiment: {sentiment_label}")
    print(f"Probabilities: {probabilities.tolist()}")

    # Accumulate probabilities for mean calculation
    if total_probabilities is None:
        total_probabilities = probabilities
    else:
        total_probabilities += probabilities

# Calculate mean probabilities
mean_probabilities = total_probabilities / len(input_id_chunks)

# Predicted sentiment for the entire text is the argmax of mean probabilities
predicted_sentiment = torch.argmax(mean_probabilities).item()

# Print overall predicted sentiment
overall_sentiment_label = sentiment_labels[predicted_sentiment]
print(f"Overall Predicted Sentiment: {overall_sentiment_label}")
print(f"Overall Probabilities: {mean_probabilities.tolist()}")