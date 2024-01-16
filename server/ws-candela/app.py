import json
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_cors import CORS, cross_origin
import signal
import threading
from queue import Queue
import requests
from cerberus import Validator
from werkzeug.serving import make_server

import os
from os import environ
import sys

script_dir = os.getcwd()
my_module_path = os.path.join(script_dir, ".")
sys.path.append(my_module_path)
os.chdir(os.path.dirname(__file__))

from webscraping import ws_app

queue_info = Queue()

app = Flask(__name__)
#cors = CORS(app, resources={r"/cups20": {"origins": "https://client-calculadora-several.thankfulgrass-02544078.westeurope.azurecontainerapps.io"}})
CORS(app)
app.config["DEBUG"] = True
limiter = Limiter(
    app,
    default_limits=["1000 per day", "50 per hour"]
)

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
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def home():
   return "API ws-candela"

@app.route('/shutdown', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def shutdown():
    """
    Endpoint for shutting down the Flask server gracefully.

    This route expects a POST request to initiate the shutdown process.

    Returns:
        object: JSON response indicating the server shutdown status.
    """
    if request.method == 'POST':
        print("Deteniendo la aplicación...")
        os.kill(os.getpid(), signal.SIGINT)
        return jsonify(message="Server shutting down..."), 200
    else:
        return jsonify(error="Invalid request method"), 405

def ws_candela(cups):
    """
    Perform web scraping for Candela information using the provided CUPS identifier.
    Args:
        cups (str): The CUPS (Código Universal del Punto de Suministro) identifier.

    Returns:
        None: The function puts the scraped information into a queue.
    """
    try:
        info = ws_app.webscraping_chrome_candelas(cups)
        queue_info.put(info)
    except Exception as e:
        queue_info.put(str(e))

@app.route('/cups20', methods=['GET'])
@limiter.limit("10 per minute")
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def calcule_energy_consumption():
    """
    Endpoint for calculating energy consumption based on a CUPS identifier.

    Returns:
        dict: JSON response containing information about the energy consumption calculation.
    """
    schema = {
    'cups20': {'type': 'string', 'minlength': 20, 'maxlength': 22},
    }
    validator = Validator(schema)

    try:
        record = json.loads(request.data)
        if validator.validate(record):
            for c in record:
                cups = record["cups20"]
                thread = threading.Thread(target=ws_candela, args=(cups,))
                thread.start()
            thread.join()
            info = queue_info.get()
            return {"info": info, 'record': record}
        else:
            return {'error': f'Data is invalid {validator.errors}'}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

if __name__ == '__main__':
  server = make_server('127.0.0.1', 5000, app)
  server.serve_forever()