import os
import requests
from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv('DATABASE_URL')
client = MongoClient(db_url)
db = client['stockwise']
collection = db['rss_feed']

app = Flask(__name__)
CORS(app)

@app.route('/ainews/<string:name>', methods=['GET'])
def main(name):
    try:
        dbresponse = list(collection.find({"name":name}, {"_id":0}))
        
        if dbresponse:
            print("found")
            return jsonify(dbresponse)
        else:
            print("not found")
            fetch_res = requests.get(f"http://localhost:4001/stock?ticker={name}")

            if fetch_res.status_code == 200:
                 response = list(collection.find({"name": name}, {"_id": 0}))
                 return jsonify(response)
            else:
                return jsonify({"error": "failed to fetch"}), 500
    except Exception as e:
        return jsonify({"error":str(e)}), 500        
    


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3001, debug=True)