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
app.config["DEBUG"] = True
limiter = Limiter(
    app,
    default_limits=["1000 per day", "50 per hour"]
)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Comtrol-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def home():
   return "API Extract Data Invoice"

    
@app.route('/invoice', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def load_pdf():    

    file = request.files['file_data']

    name_file = file.filename
    _, extension = os.path.splitext(name_file)

    if extension.lower() == ".pdf":

        pdf_data_base64 = request.files['file_data']
        response = functions.upload_pdf(pdf_data_base64)

    elif extension.lower() == ".png" or extension.lower() == ".jpeg" or extension.lower() == ".jpg":
        img_file = request.files['file_data']
        response = functions.image_to_text(img_file)

    if response:
    
        response_langchain = []
        qa_document_chain = functions.create_qa_chain()
        link_cnmc = functions.extract_link()
        if link_cnmc:
            info_cnmc = functions.extract_info_ws_cnvm(link_cnmc)
            info_cnmc["cups20"] = functions.extract_cups(link_cnmc)
            # promps = [
            #         "Dame el precio de Potencia Punta en €",
            #         "Dame el precio de Potencia valle en €",
            #         "Dame el precio de Potencia llano en €",
            #         "Dame los dias facturados"
            #         ]
            # for p in promps:
            #     qa_doc_response = functions.response_question_langchain(qa_document_chain,p)
            #     response_langchain.append(functions.invoice_clean_data(qa_doc_response))

        prizes = functions.prizes_invoice()
        all_info = {"info_cnmc": info_cnmc,
                    #"info-openai": response_langchain,
                    "days_rating": functions.extract_days(),
                    "prizes": prizes}

    return {"info": all_info}
if __name__ == '__main__':
  server = make_server('127.0.0.1', 5001, app)
  server.serve_forever()