import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load student marks from JSON file
with open(os.path.join(os.path.dirname(__file__), '../q-vercel-python.json'), 'r') as file:
    data = json.load(file)

@app.route('/api', methods=['GET'])
def get_marks():
    names = request.args.getlist('name')  # Get names from query parameters
    marks = [data.get(name, 0) for name in names]  # Get marks or default to 0
    return jsonify({"marks": marks})

# Vercel requires this for handling serverless functions
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)
