import os
import json
import time
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')
client = MongoClient(db_url)
db = client['stockwise']
collection = db['rss_feed']

def main():
    try:
        db_respose = list(collection.find_one_and_update({'name': 'aapl'}, {'_id':0}))
        if db_respose:
            print(db_respose.json())
        else:
            print('not found')

    except:
        print("error")


main()