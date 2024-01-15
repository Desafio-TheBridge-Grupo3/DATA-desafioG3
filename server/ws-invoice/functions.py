import cv2 as cv
import easyocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import fitz
from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

import time
import re
import copy
from dotenv import load_dotenv
import os
import pandas as pd

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

p_counter_kW=0
p_counter_kWh=0

def create_qa_chain(): 
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)
    qa_chain = load_qa_chain(llm, chain_type="map_reduce")
    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

    return qa_document_chain

def extract_text_from_pdf(pdf):
    try:
        doc = fitz.open(stream=pdf.read(), filetype="pdf")
        full_text = ""

        for page_num in range(doc.page_count - 1):
            page = doc[page_num]
            page_text = page.get_text()
            full_text += page_text

        with open('data/pdf/invoice.pdf', 'wb') as output_pdf:
            pdf.seek(0)
            output_pdf.write(pdf.read())

        doc.close()

        return full_text
    except Exception as e:
        return str(e)

def save_text_to_txt(text, txt_path):
    if os.path.exists(os.path.dirname(txt_path)):
        try:
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
            print(f'Archivo guardado exitosamente en: {txt_path}')
        except Exception as e:
            print(f'Error al guardar el archivo: {e}')
    else:
        print(f'La ruta especificada no existe: {os.path.dirname(txt_path)}')

def response_question_langchain(qa_document_chain, question):
    fragment_size = 4096
    all_responses= {"question": [],"response" : [], "error": []}
    with open("data/txt/invoice.txt", 'r', encoding='utf-8') as file:
        while True:
            part = file.read(fragment_size)
            if not part:
                break
            try:
                response = qa_document_chain.run(
                    input_document=part,
                    question=question,
                )
                all_responses["question"].append(question)
                all_responses["response"].append(response)
            except Exception as e:
                all_responses["error"].append(str(e))
    all_responses["question"] = all_responses["question"][0]
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
            clean_response["response"][i] = result
    return clean_response

def upload_pdf(pdf_data):
    try:

        path_txt = "data\\txt\\invoice.txt"

        # read PDF
        print(pdf_data)
        pdf_txt = extract_text_from_pdf(pdf_data)
        save_text_to_txt(pdf_txt, path_txt)

        return {'response': "Se ha subido correctamente el pdf"}
    except Exception as e:
        return {'error': f"Error al subir el pdf: {str(e)}"}
    
def extract_link():
    doc = fitz.open('data/pdf/invoice.pdf')

    for pages_num in range(doc.page_count):
        page = doc[pages_num]
        enlaces = page.get_links()

        for enlace in enlaces:
            url = enlace.get('uri')
            if url:
                return url
            else:
                return None

    doc.close()

def extract_cups(link):

    cups_pattern = re.compile(r'cups=[A-Z0-9]+')
    matches = cups_pattern.findall(link)

    cleaned_matches = [''.join(match.split()) for match in matches]

    return cleaned_matches[0][5:]

def extract_days():
    with open("data/txt/invoice.txt", 'r', encoding='utf-8') as file:
        file_txt = file.read()
    cups_pattern = re.compile(r'\b\d+\s*(?=\bdías\b)')
    matches = cups_pattern.findall(file_txt)

    if matches:
        return matches[0].replace(" ", "")
    else:
        return None

def extract_info_ws_cnvm(link_cnmc):

    info_cnmc = {
        "cups20": [],
        "start_date" : [],
        "end_date": [],
        "invoice_date": [],
        "consumption_total": [],
        "llane_consumption": [],
        "peak_consumption": [],
        "valley_consumption": []
    }

    path_driver = os.getcwd() + "\chromedriver-win64\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    servicio = Service(path_driver)
    driver = webdriver.Chrome(service=servicio, options=chrome_options)
    driver.get(link_cnmc)
    time.sleep(6)

    info_cnmc["start_date"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/section/div[1]/div[1]/div[1]/div[1]/span[2]').text
    info_cnmc["end_date"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/section/div[1]/div[1]/div[1]/div[2]/span[2]').text
    info_cnmc["invoice_date"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/section/div[1]/div[1]/div[1]/div[3]/span[2]').text
    info_cnmc["consumption_total"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/section/div[1]/div[1]/div[1]/div[7]/span[2]').text
    info_cnmc["llane_consumption"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/section/div[1]/div[1]/div[1]/div[9]/span[2]').text
    info_cnmc["peak_consumption"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/section/div[1]/div[1]/div[1]/div[8]/span[2]').text
    info_cnmc["valley_consumption"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/section/div[1]/div[1]/div[1]/div[10]/span[2]').text
    info_cnmc["peak_power"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/section/div[1]/div[1]/div[1]/div[11]/span[2]').text
    info_cnmc["valley_power"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[2]/main/div[1]/section/div[1]/div[1]/div[1]/div[12]/span[2]').text

    return info_cnmc



def image_to_text(res_img):

    try:
        img_path = "data\\txt\\invoice.txt"
        save_txt = ""

        temp_name = f"temp_image.png"
        temp_path = os.path.join("data\\image", temp_name)
        res_img.save(temp_path)

        img = cv.imread(temp_path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        reader = easyocr.Reader(['es'])
        img_txt = reader.readtext(gray)

        for n in img_txt:
            save_txt += n[1] + " "

        save_text_to_txt(save_txt, img_path)

        return {'response': "Se ha subido la imagen"}
    except Exception as e:
        return {'error': f"Error al subir la imagen: {str(e)}"}
    
def prices_invoice():
    patron = re.compile(r'\b\d+\,\d{6}\b')
    with open("data/txt/invoice.txt", 'r', encoding='utf-8') as txt_file:
        txt_file = txt_file.read()

    matches = patron.findall(txt_file)

    cleaned_matches = [''.join(match.split()) for match in matches]

    patron = r'€/kWh|€/kW'
    measured = re.findall(patron, txt_file)
    return measured,cleaned_matches

def df_create(measured, cleaned_matches):
    data = {'precios': cleaned_matches, 'unidades': measured}
    df = pd.DataFrame.from_dict(data, orient='index').transpose()
    df.dropna(inplace=True)
    return df

def assign_p_values(df):
    global p_counter_kW, p_counter_kWh
    
    if df['unidades'] == '€/kW':
        p_counter_kW += 1
        return f'p{p_counter_kW}'
    elif df['unidades'] == '€/kWh':
        p_counter_kWh += 1
        return f'p{p_counter_kWh}'
    else:
        return ''

def json_prices(df):
    pdf_scarp_info = {
    "p1_price_kw": [],
    "p2_price_kw": [],
    "p3_price_kw": [],
    "p4_price_kw": [],
    "p5_price_kw": [],
    "p6_price_kw": [],
    "p1_price_kwh": [],
    "p2_price_kwh": [],
    "p3_price_kwh": [],
    "p4_price_kwh": [],
    "p5_price_kwh": [],
    "p6_price_kwh": [],
        }

    for index, row in df.iterrows():
        price_type = f"{row['P_values']}_price_{row['unidades'][2:].lower()}"
        pdf_scarp_info[price_type].append(row['precios'])
    
    return pdf_scarp_info
