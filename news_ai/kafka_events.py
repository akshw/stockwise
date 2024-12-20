import os
import json
import time
import feedparser
import pandas as pd 
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from pymongo import MongoClient
from kafka import KafkaConsumer
from dotenv import load_dotenv


load_dotenv()
db_url = os.getenv('DATABASE_URL')
client = MongoClient(db_url)
db = client['stockwise']
collection = db['rss_feed']
df = pd.DataFrame(columns=["datetime", "title", "description", "link", "sentiment", "score"])

def aiAnalysis(payload: str):
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)
    res = classifier(payload)
    return res[0]


def main(stock):

    global df

    ticker = str(stock.lower())
    print(f"Ticker: {ticker}")
    start = time.time()

    url = 'https://finance.yahoo.com/rss/headline?s='+str(ticker)
    feed = feedparser.parse(url)

    for article in feed.entries:
        # if ticker.lower() in article.summary.lower():
        #    continue

        datetime = article.published
        title = article.title
        description = article.summary
        link = article.link

        output = aiAnalysis(title)
        sentiment = output['label']
        score = output['score']

        data = {
            'name': ticker,
            'datetime': datetime,
            'title': title,
            'description': description,
            'link': link,
            'sentiment': sentiment,
            'score': score
        }

        collection.insert_one(data)
        
        # new_row = pd.DataFrame([[datetime, title, description, link, sentiment, score]], columns=df.columns)
        # df = pd.concat([new_row, df], ignore_index=True)

    end = time.time()
    print(str(end-start)+ " seconds")

    # df.to_csv("rss_data.csv", index=False)

    return None


consumer = KafkaConsumer(
    'stock-req',
    bootstrap_servers=['localhost:9092'],
    group_id='ai-backend-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    task_data = message.value
    task_id = task_data['id']
    payload = task_data['payload']
    
    main(payload)
    
