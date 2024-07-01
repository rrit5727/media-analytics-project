from transformers import BertForSequenceClassification, BertTokenizer
import torch
import spacy
from collections import Counter

# Load tokenizer and model for sentiment analysis
tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')

# Example text
txt = """

BMW has revealed a timeline for when hydrogen cars are likely to become available in Australia, but one of the German marque’s executives says they will not replace electric vehicles.
The company – which also owns Rolls Royce and Mini – has sent two hydrogen vehicles to Australia to undergo testing in local conditions and assess market appetite.
BMW has been working on hydrogen technology for the past four decades. But Juergen Guldner, the executive in charge of developing the alternative fuel for the group, says about 15 years ago the company switched its strategy from working on a hydrogen combustion engine to fuel cell ­technology.
This means that BMW’s hydrogen cars are effectively EVs, with a chemical reaction taking place in the fuel cell between hydrogen and oxygen from the air, through which power for an electric motor is generated.
BMW Group general manager of hydrogen technology and vehicle projects Juergen Guldner.
BMW Group general manager of hydrogen technology and vehicle projects Juergen Guldner.
But Guldner says there are two key differences that should bode well for the Australian market, which involves drivers travelling long distances and towing heavy loads such as caravans, boats and horse floats. Developing hydrogen is more about offering customers choice rather than superseding battery EVs.
“With hydrogen, you drive to a fuel fuelling station. It’s the same set-up in a fuelling station, like with gasoline: you just drive there, and in three to four minutes, you’re full, 100 per cent and keep going,” he says.
This compares with fast chargers taking about 30 minutes to recharge an EV from empty.
“Towing also is a use case where you have a lot of energy consumption in the car, which means in an electric car, you have to charge often,” he says. “And to be honest, the main advantage of a hydrogen car is that you can refuel it very, very quickly. It is an electric car because it’s driven by the same electric motor. But in addition to all the advantages of electric driving, you have the advantage that you can refuel it in just three to four minutes.”
It also avoids tricky parking arrangements at charging stations that aren’t equipped for motorists towing loads. Guldner says in Europe – like some stations in Australia – people had to park elsewhere, uncouple their load, and then drive to an EV charger. “It’s simply impractical,” he says.
But to take advantage of the technology, more manufacturers need to produce hydrogen vehicles at scale, and more service stations need to stock the fuel.
Australia is making some progress in this regard. After receiving $34m from the Australian Rewable Energy Agency and $1m from the Victorian government, Viva Energy — which owns Shell branded service stations — is building a “new energies service station” in Geelong which offers hydrogen refuelling and electric charging for heavy fuel cell vehicles.
The entire project is estimated to cost $61.2m and also includes the deployment of 15 commercial hydrogen fuel cell electric vehicles.
“We, of course, need hydrogen fuelling station infrastructure. And I was really happy to see this week here in Australia that there are several projects popping up to actually build this infrastructure, bit by bit,” Guldner says.
BMW's hydrogen fuel cell in an iX5 SUV.
BMW's hydrogen fuel cell in an iX5 SUV.
BMW expects it won’t be until the early 2030s – at least – that hydrogen vehicles enter the mainstream.
“When we started with the electric vehicles, we had a pilot fleet of minis and BMW electric vehicles … that we kind of used very clearly to understand how people use electric cars. Based on that, we developed our first all-battery electric vehicle. That was only 10 years ago – we introduced it to Australia in 2014,” Guldner says.
“From that, we kind of rolled out the battery electric powertrains into all of our model line-ups. And now we have in the minis, the BMWs and the Rolls Royce, basically in every model, we have battery electric cars or battery electric powertrains with the hydrogen. We are still at this pilot phase.
“(The aim is with the pilot fleet) really to understand which countries are developing infrastructure, where is there an interest to use vehicles in the future, and based on the feedback, we will as a company make the decision – maybe this year or next year – whether it is the right time for us to actually go into mass production.”
Guldner says a similar process to the EV rollout will follow. While a hydrogen powertrain in one BMW could be developed within this decade, it would take until the early 2030s for it to become widespread across the marque’s range.
“That is kind of the three steps that we want to go through,” he says. “Pilot fleet now, gathering all kinds of information about it, how the vehicles behave, and also, especially getting feedback about the different countries, and then a one-off – the first market introduction vehicle – and the rollout later on.”
One of BMW's hydrogen powered iX5 SUVs.
One of BMW's hydrogen powered iX5 SUVs.
Despite being at the opposite side of the globe to BMW’s headquarters in Munich, Australia is a key market for the company, particularly given the Albanese government’s new vehicle efficiency standard, which takes effect next year, Guldner says.
“Australia is a key focus for our program, firstly because of the important steps the country is taking in decarbonising its vehicle fleet. However, the country is also an interesting study due to its varied driving conditions and the long distances covered between towns and cities. With the appropriate infrastructure, an FCEV (fuel cell electric vehicle) would make a strong mobility case due to its range capability and short refuelling time.”
Asked why BMW switched from developing a hydrogen combustion engine to a fuel cell vehicle, Guldner says it was all about range.
He says the pilot vehicles in Australia can achieve more than 500km of driving range from six kilograms of hydrogen versus 300km from a hydrogen combustion engine with the same sized fuel tank.
“We cannot sell a car that has 300km (driving range), so that’s why we abandoned the combustion engine. Combustion engines might be OK for trucks because they operate at a steady state — driving at the same speed for hours and hours on end, where the efficiency can be optimised,” he says.
“The difference in a passenger car is we have a lot of transient behaviour, so we would get in a passenger car only 300km.”
In the pilot vehicles, the hydrogen fuel cell system and a high-performance battery combine to generate a maximum output of 295kW. Two carbon-fibre-reinforced plastic tanks together hold about six kilograms of gaseous hydrogen, enabling quick refilling.
The pilot vehicles will be in Australia until November.
More Coverage
This car could be an EV tipping point
This car could be an EV tipping point
This car has everything — including a great left hook
This car has everything — including a great left hook



"""

# Load spaCy for NER
nlp = spacy.load('en_core_web_sm')

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

# NER tags to extract
ner_tags = ['ORG', 'PERSON', 'GPE']  # Organization, Person, Geopolitical Entity

# Extract entities from the text
doc = nlp(txt)
entities = [ent.text for ent in doc.ents if ent.label_ in ner_tags]

# Count occurrences of each entity
entity_counts = Counter(entities)
most_common_entities = entity_counts.most_common(2)

print("Top 2 most mentioned entities:")
for i, (entity, count) in enumerate(most_common_entities, start=1):
    print(f"{i}. Entity: {entity}, Count: {count}")

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