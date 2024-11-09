import os
import requests
from flask import Flask, request
from bs4 import BeautifulSoup
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')


client = MongoClient(db_url)
db = client['stockwise']
collection = db['news_feed1']


df = pd.DataFrame(columns=["datetime", "title", "link", "sentiment", "score"])


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
    

    for page in range(1):
        url = f'https://markets.businessinsider.com/news/{ticker}-stock?p={page}'
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        
        articles = soup.find_all('div', class_='latest-news__story')
        
        for article in articles:
            datetime = article.find('time', class_='latest-news__date').get('datetime')
            title = article.find('a', class_='news-link').text
            link = article.find('a', class_='news-link').get('href')
            
            output = aiAnalysis(title)
            sentiment = output['label']
            score = output['score']
            
            data = {
                'datetime': datetime,
                'name': ticker,
                'title': title,
                'link': link,
                'sentiment': sentiment,
                'score': score
            }
            
            collection.insert_one(data)
            

            new_row = pd.DataFrame([[datetime, title, link, sentiment, score]], columns=df.columns)
            df = pd.concat([new_row, df], ignore_index=True)


    # df.to_csv("scraped_data.csv", index=False)
    return "Scraping and analysis complete", 200



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000, debug=True)
