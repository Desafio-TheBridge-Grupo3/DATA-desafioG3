import json
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_cors import CORS, cross_origin
import signal
import threading
from queue import Queue
from cerberus import Validator
from werkzeug.serving import make_server

import os
import functions

app = Flask(__name__)
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
   return "API Extract Data Invoice"

    
@app.route('/invoice', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def load_pdf():    
    """
    Endpoint for processing and extracting information from PDF or image files.

    Returns:
        dict: JSON response containing extracted information from the uploaded file.
    """
    file = request.files['file_data']
    info_link = {}

    name_file = file.filename
    _, extension = os.path.splitext(name_file)

    if extension.lower() == ".pdf":

        pdf_data_base64 = request.files['file_data']
        response = functions.upload_pdf(pdf_data_base64)

    elif extension.lower() == ".png" or extension.lower() == ".jpeg" or extension.lower() == ".jpg":
        img_file = request.files['file_data']
        response = functions.image_to_text(img_file)

    if response:
    
        link_cnmc = functions.extract_link()
        if link_cnmc:
            info_link = functions.extract_link_info(link_cnmc)
        
        measured,cleaned_matches = functions.prices_invoice()
        df = functions.df_create(measured, cleaned_matches)
        df['P_values'] = df.apply(functions.assign_p_values, axis=1)
        price = functions.json_prices(df)
        functions.p_counter_kW=0
        functions.p_counter_kWh=0

    if info_link:
        all_info = {"info_cnmc": info_link,
                    "prices": price}
        
    else:
        all_info = {"info_cnmc": "",
                    "prices": price}

    return {"info": all_info}
if __name__ == '__main__':
  server = make_server('127.0.0.1', 5001, app)
  server.serve_forever()