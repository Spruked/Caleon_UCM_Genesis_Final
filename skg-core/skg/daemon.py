import argparse
from flask import Flask, request, jsonify
from .core import SKGService

app = Flask(__name__)
skg = None

@app.route('/add', methods=['POST'])
def add_triple():
    data = request.json
    skg.add(data['sub'], data['pred'], data['obj'], data.get('weight', 1.0))
    return jsonify({'status': 'added'})

@app.route('/query', methods=['POST'])
def query():
    pat = request.json['pattern']
    k = request.json.get('k', 10)
    results = skg.query(pat, k)
    return jsonify(results)

def main():
    global skg
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="ucm_skg.db")
    parser.add_argument("--port", type=int, default=7777)
    args = parser.parse_args()
    skg = SKGService(db_path=args.db)
    app.run(host='0.0.0.0', port=args.port, debug=True)

if __name__ == "__main__": main()