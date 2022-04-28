from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import os, sys
import requests
from invokes import invoke_http
from os import environ
import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

# Change these url:
order_URL = environ.get('order_URL') or "http://localhost:5005/order"

@app.route("/place_order", methods=['POST'])
def place_order():
    if request.is_json:
        try:
            order_data = request.get_json()
            try:
                jwt_data = jwt.decode(order_data['jwt_token'], "esd_is_so_fun_omg123", algorithms="HS256")
            except jwt.exceptions.InvalidSignatureError:
                return jsonify({
                    "code": 400,
                    "message": "Invalid token signature"
                }), 400
            order_result = invoke_http(order_URL, method='POST', json=order_data)
            if order_result[0]['code'] != 200:
                amqp_setup.channel.basic_publish(exchange="order_topic", routing_key="order.error", body=order_result['message'], properties=pika.BasicProperties(delivery_mode = 2))
            amqp_setup.channel.basic_publish(exchange="order_topic", routing_key="order", body=json.dumps(order_data), properties=pika.BasicProperties(delivery_mode = 2))
            amqp_setup.channel.basic_publish(exchange="order_topic", routing_key="order.notify", body=json.dumps(order_data), properties=pika.BasicProperties(delivery_mode = 2))
            return jsonify({
                "code": 200,
                "data": order_result[0]['data']
            }), 200

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)
