import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import easyocr

import fitz
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

import re
import copy
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_qa_chain(): 
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
    qa_chain = load_qa_chain(llm, chain_type="map_reduce")
    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

    return qa_document_chain

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(doc.page_count - 1):
        page = doc[page_num]
        page_text = page.get_text()
        full_text += page_text

    doc.close()

    return full_text

def save_text_to_txt(text, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def response_question_langchain(qa_document_chain, question):
    fragment_size = 4096
    all_responses= {"question": [],"response" : [], "error": []}
    with open("invoice.txt", 'r', encoding='utf-8') as file:
        while True:
            part = file.read(fragment_size)
            if not part:
                break
            try:
                response = qa_document_chain.run(
                    input_document=part,
                    question=question,
                )
                all_responses["response"].append(response)
            except Exception as e:
                all_responses["error"].append(str(e))
    return all_responses

def invoice_clean_data(response):
    clean_response = copy.deepcopy(response)
    float_patron = r'\b\d+[.,]\d+\b'
    not_answer = ["lo siento","no se", "no puedo", "no se menciona"]
    for i,r in enumerate(response["response"]):
        if any(word.lower() in r.lower() for word in not_answer):
            clean_response["response"][i] = " "
        else:
            result = re.findall(float_patron,r)
            result = result[0].replace(",",".")
            clean_response["response"][i] = result
    return clean_response