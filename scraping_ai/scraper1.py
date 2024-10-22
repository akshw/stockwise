import feedparser
from transformers import pipeline

pipe = pipeline("text-classification", model="ProsusAI/finbert")

ticker  = 'META'
keyword = 'meta'

url = 'https://finance.yahoo.com/rss/headline?s='+str(ticker)

feed = feedparser.parse(url)

score = 0
articles = 0

for i, entry in enumerate(feed.entries):
    if keyword.lower() in entry.summary.lower():
        continue

    print('Title:'+ str(entry.title))
    print('link:'+ str(entry.link))
    print('published:'+ str(entry.published))
    print('Summary:'+ str(entry.summary))

    sentiment = pipe(entry.summary)[0]

    print(sentiment['label'], sentiment['score'])
    print('-' * 30)

    if sentiment['label'] == 'positive':
        score += sentiment['score']
        articles += 1
    elif sentiment['label'] == 'negative':
        score -= sentiment['score'] 
        articles += 1

finalScore = score/articles
print(finalScore)
