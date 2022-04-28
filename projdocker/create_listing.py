from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import os, sys
import requests
from invokes import invoke_http
from os import environ

app = Flask(__name__)
CORS(app)

account_URL = environ.get('account_URL') or "http://localhost:8000/graphql"
listing_URL = environ.get('listing_URL') or "http://localhost:5000/listing"

@app.route("/create_listing", methods=['POST'])
def create_listing():
    if request.is_json:
        data = request.get_json()
        selleremail = data['selleremail']
        qdict = {}
        qdict['query'] = "query {user (em: \"" + selleremail + "\") {fullname}}"
        result = invoke_http(account_URL, method='POST', json=qdict)
        if result:
            data['sellername'] = result['data']['user']['fullname']
            finalresult = invoke_http(listing_URL, method='POST', json=data)
            if finalresult:
                return jsonify({
                    "code": 201,
                    "message": "Post created successfully!"
                }), 201
            else:
                return jsonify({
                    "code": 400,
                    "message": "Internal server error"
                }),
        else:
            return jsonify({
                "code": 400,
                "message": "Invalid JSON input: " + str(request.get_data())
            }),

    # if not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
