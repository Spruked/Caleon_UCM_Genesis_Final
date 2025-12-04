from flask import Flask, request, jsonify
from .core import SKGService

app = Flask(__name__)
skg = SKGService()

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)