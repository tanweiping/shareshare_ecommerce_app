#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ
import amqp_setup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/esd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)

monitorBindingKey='*.error'

class Error(db.Model):
    __tablename__ = 'error'

    error_id = db.Column(db.Integer, primary_key=True)
    # category = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    def json(self):
        # return {'error_id': self.error_id, 'category': self.category, 'description': self.description}
        return {'error_id': self.error_id, 'description': self.description}

def receiveError():
    amqp_setup.check_setup()

    queue_name = "Error"

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages;
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an error by " + __file__)
    processError(body)
    print() # print a new line feed


def processError(errorMsg):
    print("Printing the error message:")
    try:
        error = json.loads(errorMsg)
        print("--Message JSON:", error['message'])
        final_error = Error(description=error['message'])

        db.session.add(final_error)
        db.session.commit()

    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
    print()


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveError()
