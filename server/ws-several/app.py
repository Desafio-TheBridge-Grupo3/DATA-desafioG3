import json
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_cors import CORS, cross_origin
from cerberus import Validator
import requests
from werkzeug.serving import make_server

import os
from os import environ
import sys
import functions

script_dir = os.getcwd()
my_module_path = os.path.join(script_dir, ".")
sys.path.append(my_module_path)
os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True
limiter = Limiter(
    app,
    default_limits=["1000 per day", "50 per hour"]
)
CORS(app)

@app.after_request
def after_request(response):
    """
    A decorator to add headers to the HTTP response for enabling Cross-Origin Resource Sharing (CORS).
    Args:
        response (object): The HTTP response object.

    Returns:
        object: The modified HTTP response object.
    """
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Comtrol-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def home():
   return "API ws-several"

@app.route('/filter_several', methods=['GET'])
@limiter.limit("100 per minute")
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def filter_info():
    """
    Receives a configuration as a JSON payload and filters the database based on the provided criteria.
    
    The function validates the input configuration against a predefined JSON schema and,
    if the validation passes, it establishes a connection to the database using the
    'my_connection' function from the 'functions' module. It then calls the 'con_filter_info'
    function to perform the actual filtering in the database and retrieve the prices of tariffs.
    
    Args:
        None (uses request.data): JSON payload containing the filter configuration.

    Returns:
        dict: A JSON response containing the filtered information or an error message.
    """
    schema = {
    'cia': {'type': 'string', 'minlength': 1, 'maxlength': 100},
    'zone': {'type': 'string', 'minlength': 1, 'maxlength': 50},
    'rate': {'type': 'string', 'minlength': 1, 'maxlength': 10},
    'indexed_date': {'type': 'string', 'minlength': 1, 'maxlength': 100},
    'fee': {'type': 'string', 'minlength': 1, 'maxlength': 100},
    'product_cia': {'type': 'string', 'minlength': 1, 'maxlength': 100},
    'market': {'type': 'string', 'minlength': 1, 'maxlength':10},
    }
    validator = Validator(schema)

    try:
        record = json.loads(request.data)
        if validator.validate(record):
            connection = functions.my_connection()
            response = functions.con_filter_info(connection, record)

            return {"response": response}

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    
if __name__ == '__main__':
  server = make_server('0.0.0.0', 5002, app)
  server.serve_forever()