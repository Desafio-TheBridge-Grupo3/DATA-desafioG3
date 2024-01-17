# API Extract Data Invoice

Esta API proporciona un servicio para procesar y extraer información de archivos PDF o imágenes. La aplicación carga un archivo, ya sea en formato PDF o imagen (PNG, JPEG, JPG), y extrae información relevante, incluyendo detalles sobre precios y enlaces CNMC.

## Instrucciones de Uso

### Instalación de Dependencias
Asegúrate de tener las siguientes bibliotecas de Python instaladas:

```bash
pip install -r requirements.txt
```

## Ejecución de la Aplicación
Ejecuta el script app.py para iniciar el servidor Flask.

```bash
python app.py
```

El servidor se iniciará en http://127.0.0.1:5001/

## Endpoints

- Endpoint: http://127.0.0.1:5001/invoice
- Método: POST 
- Descripción: Procesa y extrae información de archivos PDF o imágenes de facturas de energéticas.
- Parámetros de Entrada: Archivos .PDF o imagen en .PNG, .JPG o .JPEG.
- Respuesta:
    - Exitosa:
        ```bash
            {
                "info": {
                    "info_cnmc": {
                    "cups20": "XXXXX",
                    "end_date": "XXXXX",
                    "invoice_date": "XXXXX",
                    "peak_power": "XXXXX",
                    "start_date": "XXXXX",
                    "valley_power": "XXXXX"
                    },
                "prices": {
                    "p1_price_kw": ["XXXXX"],
                    "p1_price_kwh": ["XXXXX"],
                    "p2_price_kw": ["XXXXX"],
                    "p2_price_kwh": ["XXXXX"],
                    "p3_price_kw": ["XXXXX"],
                    "p3_price_kwh": ["XXXXX"],
                    "p4_price_kw": ["XXXXX"],
                    "p4_price_kwh": ["XXXXX"],
                    "p5_price_kw": ["XXXXX"],
                    "p5_price_kwh": ["XXXXX"],
                    "p6_price_kw": ["XXXXX"],
                    "p6_price_kwh": ["XXXXX"]
                    }
                }
            }
        ```
    - Error:
        ```bash
            { "error": "Mensaje de error"}
        ```

## Notas Importantes

Asegúrate de que las dependencias estén instaladas antes de ejecutar la aplicación.

El servidor se inicia en http://127.0.0.1:5001/ por defecto.

La API utiliza CORS para permitir solicitudes desde cualquier origen ('*').