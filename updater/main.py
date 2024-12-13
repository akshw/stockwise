import os
import json
import time
import logging
from pymongo import MongoClient
from dotenv import load_dotenv
from contextlib import contextmanager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

@contextmanager
def get_db_connection():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    client = None
    try:
        client = MongoClient(db_url)
        yield client['stockwise']
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise
    finally:
        if client:
            client.close()

def get_all_names():
    try:
        with get_db_connection() as db:
            collection = db['rss_feed']
            cursor = collection.find({}, {'name': 1, '_id': 0})
            names = [doc['name'] for doc in cursor]
            logging.info(f"Successfully retrieved {len(names)} names")
            return names
    except Exception as e:
        logging.error(f"Error retrieving names: {e}")
        return []

def main():
    try:
        names = get_all_names()
        if names:
            logging.info(f"Found {len(names)} names: {names}")
        else:
            logging.warning("No names found")
    except Exception as e:
        logging.error(f"Main execution error: {e}")

if __name__ == '__main__':
    main()