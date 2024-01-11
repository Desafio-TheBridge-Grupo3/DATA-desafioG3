import json
from flask import Flask, request, jsonify
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def calcule_energy_consumption():
    record = json.loads(request.data)
    
    return "Welcome to mi API conected to my books database"