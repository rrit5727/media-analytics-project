from transformers import pipeline

# source myenv/bin/activate - activate virtual environment if necessary

# Specify the model 
model_name = "bert-large-uncased"

sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)

result = sentiment_pipeline("""Australia’s private wealth managers and stockbroking firms are a “fertile hunting ground” for global trading technology group ViewTrade, as it targets growth in a market that is expected to have about $9 trillion in superannuation by 2041.
Having just kicked off its Australian operations, ViewTrade is helmed by Nigel Singh, platform business Integrated’s former ­operating chief and a former manager at Morgan Stanley Wealth Management.
ViewTrade – which counts Morningstar, Citic Securities and Maybank among its global customers – will use Sydney as its regional headquarters to pursue expansion in the Asia-Pacific and India.
Mr Singh said the company had identified opportunities in Australia to partner with banks, brokers, wealth managers, fintechs, super funds and family ­offices on their trading, support and brokerage technology. That was particularly the case if they were facilitating or seeking to help their own customers with cross-border and multi-asset ­investments.
“A big part of our business is making sure we do the little things right. And so we’ve got to make sure that we do this (expansion) in a sustainable, smart way,” he said.
However, Mr Singh is mindful of the challenges that come with getting traction in Australia, where many large players and financial institutions develop their own technology in-house or have established agreements with investment banks or other providers for trading technology services.
Globally, ViewTrade competes with companies such as BNY Pershing in areas such as global trading services and execution.
“The top bulge bracket investment banks that have operations here in Australia, obviously that’s going to be difficult for us, in terms of the execution piece. But from a wealth management technology piece, we can assist,” Mr Singh said. “The next tier of wealth managers in Australia … that don’t have that institutional connectivity that they used to, that’s a fertile hunting ground.”
However, consolidation and cost pressures have been top of mind in the past five years. The private wealth sector in Australia has experienced a wave of dealmaking led by international suitors. Focus Financial Partners acquired a strategic stake in Escala in 2019, while Crestone was acquired by a unit of the Princely family of Liechtenstein, LGT International, in 2022. The stockbroking industry has seen continued margin pressure and rationalisation, including Canaccord Genuity acquiring Patersons Securities in 2019, while in retail banking ANZ is in the process of buying Suncorp’s banking arm.
ViewTrade’s global chief executive, Tony Petrilli, said the company had conducted several fact-finding visits to Australia, including one last year that he was part of.
“Connectivity is important and every market is built around their local market,” Mr Petrilli said.
“Where we can help first and foremost is helping to solve some of the inefficiencies that we saw in Australia, which are no different to any other market we’ve gone to in terms of being able to access other markets without having to open the account in that other country.
“We expect to be an important player for them (brokers, wealth managers, advisory firms and super funds) in terms of giving them access to the global markets and inversely bringing non-Australian investors to the Australian market which they would benefit from as well.”
As at December 31, ViewTrade had more than $US20bn in assets under administration globally. In cross-border transactions, it brokered $US860.9bn in equity orders between 2020 and 2023.
Australia marks the 30th country where ViewTrade, founded in 2000, provides its services.
A dearth of Australian initial public offerings in recent years and a spike in investor interest in artificial intelligence and technology stocks has led to more trading by Australians in global markets.
Still, it may be a slow burn for ViewTrade in Australia as it seeks to get its business off the ground.
Mr Singh said ViewTrade had signed its first customer in Australia, an institutional wholesale dealer, but was unable to disclose the name. He expected a further two customers to take up ViewTrade services by the end of July.
“We have a strong, committed pipeline,” he said. “There are strong incumbents in the region … We think, though, that our technology can help certain slivers of the market.”
ViewTrade’s analysis estimates that “simple transformations” within Australia’s wealth management industry could create savings of $US160m annually when considering the $US474bn turnover of equities held by Australian accounts in the US. Those savings partly come from ViewTrade’s ability to aggregate trades.
The company’s local entity, ViewTrade International Australia, will hold accounts in this market and also be used to expand the firm’s APAC and India presence. It has also proposed expansion into the Middle East following that.
ViewTrade’s local team includes operating chief Carl Brazendale, a former GBST and Pershing manager, while Kerri Buggy, a former ClearBank analyst and manager at FinClear and Morgan Stanley, has joined in operations.
Deloitte has predicted Australia’s $3.9 trillion superannuation pool will balloon to more than $9 trillion by 2041, putting the nation’s pension market firmly on the radar of offshore-based companies""")

print(result)
