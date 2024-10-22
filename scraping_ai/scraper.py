import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')


client  = MongoClient(db_url)
db = client['stockwise']
collection = db['news_feed1']


columns = ['datetime', 'title', 'link', 'sentiment', 'score']
df = pd.DataFrame(columns=columns)


def aiAnalysis(payload):
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    classifier = pipeline('text-classification', model = model, tokenizer = tokenizer)
    res = classifier(payload)
    return res[0]


counter = 0
stock = input('enter stockticker name:')
ticker = str(stock.lower())
for page in range(1, 2):
    url = 'https://markets.businessinsider.com/news/'+ticker+'-stock?p='+str(page)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    articles = soup.find_all('div', class_= 'latest-news__story')

    for article in articles:
        datetime = article.find('time', class_ = 'latest-news__date').get('datetime')
        title = article.find('a', class_='news-link').text
        link = article.find('a', class_ = 'news-link').get('href')

        output = aiAnalysis(title)
        sentiment = output['label']
        score = output['score']

        data = {
            'datetime': datetime,
            'name':ticker,
            'title':title,
            'link':link,
            'sentiment':sentiment,
            'score':score
        }

        collection.insert_one(data)

        df = pd.concat([pd.DataFrame([[datetime, title, link, sentiment, score]], columns=df.columns), df], ignore_index=True)
        counter += 1
        

print(str(counter)+" articles of " +str(stock)+ " scraped and analysed")
df.to_csv("/home/lokesh/Desktop/projects/stockwise/scraping_ai/scrapedata.csv")
