## Información de la Aplicación

Esta aplicación, desarrollada con Streamlit, proporciona información detallada sobre facturas utilizando un archivo de entrada. La aplicación utiliza un endpoint para realizar cálculos y obtener información relevante sobre la factura. A continuación, se proporciona una guía sobre cómo usar la aplicación.

### Instrucciones de Uso

1. **Subir Archivo:**
   - Haz clic en el botón "Seleccionar archivo" para cargar un archivo. Asegúrate de que sea un archivo en formato `jpg`, `jpeg`, `png` o `pdf`.

2. **Llamar al Endpoint:**
   - Después de cargar el archivo, puedes hacer clic en el botón "Llamar al Endpoint con Archivo" para enviar el archivo al endpoint y obtener información sobre la factura.

3. **Espera:**
   - La aplicación mostrará un mensaje de espera mientras procesa la información. Este proceso puede tomar algunos segundos.

4. **Resultados:**
   - Una vez completado el proceso, la aplicación mostrará una tabla con información detallada sobre la factura, incluyendo datos del archivo, información CNMC y precios.

### Requisitos Previos

Asegúrate de tener Python y las bibliotecas necesarias instaladas. Puedes instalar las dependencias utilizando el siguiente comando:

```bash
RUN pip install -r requirements.txt
```
## Endpoints
```bash
GET "http://localhost:5000/cups20"
Ejemplo json = {"cups20": "XXXXXXXXXXXXXXXXXXXXXX"}
Respuesta 

