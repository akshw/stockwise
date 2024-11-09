import os
import requests
import json
import threading
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

@app.route('/ainews/<string:name>', methods=['GET'])
def main(name):
    try:
        dbresponse = list(collection.find({"name":name}, {"_id":0}))
        
        if dbresponse:
            print("found")
            return jsonify(dbresponse)
        else:
            print("not found")
            data = name
            id = name
            producer.send('stock-req', value={'id': id, 'payload':data['payload']})
            producer.flush()

            def wait_for_response(id):
                print("here")
                for message in res_consumer:
                    res_data = message.value
                    if res_data.get('id') == id:
                        response[id] = res_data['result']
                        break

        threading.Thread(target=wait_for_response(id)).start()

        while id not in response:
            pass

        return jsonify({"id": id, "result": response.pop(id)})


            # fetch_res = requests.get(f"http://localhost:4001/stock?ticker={name}")

            # if fetch_res.status_code == 200:
            #      response = list(collection.find({"name": name}, {"_id": 0}))
            #      return jsonify(response)
            # else:
            #     return jsonify({"error": "failed to fetch"}), 500
    except Exception as e:
        return jsonify({"error":str(e)}), 500        
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3001, debug=True)