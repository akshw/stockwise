import os
import requests
import json
import threading
import time
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from kafka import KafkaProducer, KafkaConsumer
from queue import Queue
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')
client = MongoClient(db_url)
db = client['stockwise']
collection = db['rss_feed']

app = Flask(__name__)
CORS(app)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/ainews/<string:name>', methods=['GET'])
def main(name):
    try:
        dbresponse = list(collection.find({"name":name}, {"_id":0}))
        
        if dbresponse:
            print("found")
            return jsonify(dbresponse)
        else:
            print("not found")
            producer.send('stock-req', value={'id': name, 'payload': name})
            producer.flush()

            time.sleep(20)
            count = 0
            while count in range(0, 20):
                try:
                    dbresponse = list(collection.find({"name":name}, {"_id":0}))
        
                    if dbresponse:
                        print("found")
                        return jsonify(dbresponse)
                    else:
                        count+=1
                        time.sleep(2)
                except:
                    print("error")
                    
            

            


            

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error":str(e)}), 500        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3001, debug=True)