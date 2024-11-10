import os
import feedparser
import pandas as pd 
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from pymongo import MongoClient
from flask import Flask, request
from kafka import KafkaConsumer, KafkaProducer
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


app = Flask(__name__)

@app.route('/stock', methods=['GET'])
def main():

    global df

    stock_input = request.args.get('ticker')
    ticker = str(stock_input.lower())
    print(f"Ticker: {ticker}")

    url = 'https://finance.yahoo.com/rss/headline?s='+str(ticker)
    feed = feedparser.parse(url)

    for article in feed.entries:
        # if ticker.lower() in article.summary.lower():
        #    continue

        datetime = article.published
        title = article.title
        description = article.summary
        link = article.link

        output = aiAnalysis(title+description)
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
        
        new_row = pd.DataFrame([[datetime, title, description, link, sentiment, score]], columns=df.columns)
        df = pd.concat([new_row, df], ignore_index=True)

    # df.to_csv("rss_data.csv", index=False)
    return "rss feed analysis complete", 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4001, debug=True)
