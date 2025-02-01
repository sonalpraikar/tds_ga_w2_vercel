# # import json
# # import os
# # from flask import Flask, request, jsonify
# # from flask_cors import CORS

# # app = Flask(__name__)
# # CORS(app)  # Enable CORS for all routes

# # # Load student marks from JSON file
# # with open(os.path.join(os.path.dirname(__file__), '../q-vercel-python.json'), 'r') as file:
# #     data = json.load(file)

# # @app.route('/api', methods=['GET'])
# # def get_marks():
# #     names = request.args.getlist('name')  # Get names from query parameters
# #     marks = [data.get(name, 0) for name in names]  # Get marks or default to 0
# #     return jsonify({"marks": marks})

# # # Vercel requires this for handling serverless functions
# # def handler(event, context):
# #     return app(event, context)

# # if __name__ == '__main__':
# #     app.run(debug=True)
# import json
# import os
# from http.server import BaseHTTPRequestHandler
# from urllib.parse import urlparse, parse_qs

# class handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS for all origins
#         self.end_headers()

#         # Load student data (replace with your actual loading method)
#         try:
#             with open('q-vercel-python.json', 'r') as f:  # Assuming the file is in the same directory
#                 student_data = json.load(f)
#         except FileNotFoundError:
#             self.wfile.write(json.dumps({"error": "Data file not found"}).encode('utf-8'))
#             return

#         query_params = parse_qs(urlparse(self.path).query)
#         names = query_params.get('name', [])  # Get list of names from query parameters
#         marks = []

#         for name in names:
#             name = name.strip()  # Remove leading/trailing spaces
#             if name in student_data:
#                 marks.append(student_data[name])
#             else:
#                 marks.append(0)  # Or handle the case where the name isn't found

#         response_data = {"marks": marks}
#         self.wfile.write(json.dumps(response_data).encode('utf-8'))

import json
from http.server import BaseHTTPRequestHandler
import urllib.parse

# Load student data from the JSON file
def load_data():
    with open('q-vercel-python.json', 'r') as file:
        data = json.load(file)
    return data

# Handler class to process incoming requests
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the query parameters
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        # Get 'name' parameters from the query string
        names = query.get('name', [])

        # Load data from the JSON file
        data = load_data()

        # Prepare the result dictionary
        result = {"marks": []}
        for name in names:
            # Find the marks for each name
            for entry in data:
                if entry["name"] == name:
                    result["marks"].append(entry["marks"])

        # Send the response header
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS for any origin
        self.end_headers()

        # Send the JSON response
        self.wfile.write(json.dumps(result).encode('utf-8'))
