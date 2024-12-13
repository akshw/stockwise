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

def get_all_names():
    try:
        # Find all documents and project only the 'name' field
        cursor = collection.find({}, {'name': 1, '_id': 0})
        # Extract names into a list
        names = [doc['name'] for doc in cursor]
        return names
    except Exception as e:
        print(f"Error retrieving names: {e}")
        return []

def main():
    names = get_all_names()
    if names:
        print(f"Found {len(names)} names: {names}")
    else:
        print("No names found or error occurred")

main()