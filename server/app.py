import json
from flask import Flask, request, jsonify
import os
from os import environ
import sys

script_dir = os.getcwd()
my_module_path = os.path.join(script_dir, "..")
sys.path.append(my_module_path)

from webscraping import ws_app

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
   return "API"

@app.route('/cups20', methods=['GET'])
def calcule_energy_consumption():
    record = json.loads(request.data)
    print(record)
    cups20 = record["cups20"]
    info = ws_app.webscraping_chrome_candelas(cups20)
    return {"info": info}

if __name__ == '__main__':
  app.run(debug = True, host = '0.0.0.0', port=environ.get("PORT", 5000))