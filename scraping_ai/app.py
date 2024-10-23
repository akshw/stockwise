from flask import Flask, request

app = Flask(__name__)

@app.route('/stock', methods = ['GET'])
def main():
    stock = request.args.get('ticker')

    if stock:
        return stock
    else:
        return "No ticker provided", 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True )