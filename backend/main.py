import os
import requests
import json
import threading
import time
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from kafka import KafkaProducer, KafkaConsumer
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

res_consumer = KafkaConsumer(
    'stock-req',
    bootstrap_servers=['localhost:9092'],
    group_id='main-backend-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
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

            start_time = time.time()

        while True:
            for message in res_consumer:
                print(message)
                if message.value.get("response") == name:
                    print("c")

            if time.time() - start_time > 5:
                return {"error": "Request timed out"}

            time.sleep(0.2)

            

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error":str(e)}), 500        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3001, debug=True)