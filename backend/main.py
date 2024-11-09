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
    'response',
    bootstrap_servers=['localhost:9092'],
    group_id='main-backend-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

response = {}

def wait_for_response(id):
    print("here")
    for message in res_consumer:
        res_data = message.value
        if res_data.get('id') == id:
            response[id] = res_data['result']
            break

@app.route('/ainews/<string:name>', methods=['GET'])
def main(name):
    try:
        dbresponse = list(collection.find({"name":name}, {"_id":0}))
        
        if dbresponse:
            print("found")
            return jsonify(dbresponse)
        else:
            print("not found")
            # Fixed: Send the name directly as payload
            producer.send('stock-req', value={'id': name, 'payload': name})
            producer.flush()

            print("a")
            # Fixed: Proper thread creation
            thread = threading.Thread(target=wait_for_response, args=(name,))
            thread.daemon = True
            thread.start()
            print("b")

            # Add timeout to prevent infinite loop
            timeout = 30  # seconds
            start_time = time.time()
            while name not in response:
                if time.time() - start_time > timeout:
                    return jsonify({"error": "Request timed out"}), 408
                time.sleep(0.1)  # Prevent CPU spinning

            return jsonify({"id": name, "result": response.pop(name)})

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Added for debugging
        return jsonify({"error":str(e)}), 500        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3001, debug=True)