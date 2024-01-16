import streamlit as st
import pandas as pd
import streamlit.components.v1 as c
import requests
import json


# Ass visual files

st.set_page_config(page_title="INFORMACÍ0N FACTURA",
                   page_icon="favicon.ico")

st.title("INFORMACÍ0N FACTURA")

st.session_state.file= st.file_uploader("Selecciona una archivo", type=["jpg", "jpeg", "png", "pdf"])

def call_endpoint(url,data):

    try:
        if isinstance(data, st.runtime.uploaded_file_manager.UploadedFile):
            files = {"file_data": data}
            response = requests.post(url, files=files)
        else:
            response = requests.get(url, data=json.dumps(data), headers={"Content-Type": "application/json"})


        if response.status_code == 200:
            st.success("Llamada al endpoint exitosa")
            st.json(response.json())
            return response.json()
        else:
            st.error(f"Fallo al llamar al endpoint. Código de respuesta: {response.status_code}")

    except Exception as e:
        st.error(f"Error: {e}")

# Botón para llamar al endpoint con el archivo
if st.button("Llamar al Endpoint con Archivo") and st.session_state.file:
    url = "http://127.0.0.1:5001/invoice"
    response = call_endpoint(url,st.session_state.file)
    cups20 = {"cups20": str(response["info"]["info_cnmc"]["cups20"])}
    url_ws = "https://ws-candela-calculadora-several.thankfulgrass-02544078.westeurope.azurecontainerapps.io/cups20"
    response_cups = call_endpoint(url_ws,cups20)


