from flask import Flask, jsonify, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/results', methods=['GET'])
def get_results():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'backend', 'results.json')
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='application/json')
        else:
            return jsonify({"error": "results.json not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)