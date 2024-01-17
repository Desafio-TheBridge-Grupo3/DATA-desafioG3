# API ws-candela

Esta API ws-candela proporciona un servicio para calcular el consumo de energía basado en un identificador CUPS (Código Universal del Punto de Suministro). La aplicación utiliza web scraping para obtener información sobre Candela.

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

El servidor se iniciará en http://127.0.0.1:5000/home

## Endpoints

- Endpoint: http://127.0.0.1:5000/cups20
- Método: POST 
- Descripción: Calcula el consumo de energía basado en un identificador CUPS proporcionado.
- Parámetros de Entrada: Se espera un objeto JSON con un campo llamado "cups20" que contiene el identificador CUPS.
    - Ejemplo JSON: `{"cups20": "XXXXXXXXXXXXXXXXXXXXXX"}`
- Límite de Rate: 10 peticiones por minuto.
- Respuesta:
    - Exitosa:
        ```bash
       {"info": {
            "anual_consumption": "XXXXX",
            "anual_consumption_p1": "XXXXX",
            "anual_consumption_p2": "XXXXX",
            "anual_consumption_p3": "XXXXX",
            "anual_consumption_p4": "XXXXX",
            "anual_consumption_p5": "XXXXX",
            "anual_consumption_p6": "XXXXX",
            "anual_power_p1": "XXXXX",
            "anual_power_p2": "XXXXX",
            "anual_power_p3": "XXXXX",
            "anual_power_p4": "XXXXX",
            "anual_power_p5": "XXXXX",
            "anual_power_p6": "XXXXX",
            "rate": "XXXXX"            
            },
        "record": {
            "cups20": "XXXXXXXXXXXXXXXXXXXXXX"
            }
        }
        ```
    - Error:
        ```bash
            { "error": "Mensaje de error"}
        ```

- Endpoint: http://127.0.0.1:5000/shutdown
- Método: POST 
- Descripción: Endpoint para parar la ejecución del servicio.
- Respuesta:
    - Exitosa:
        ```bash
        {
            "message": "Server shutting down..."
        }
        ```
## Notas Importantes

Asegúrate de que las dependencias estén instaladas antes de ejecutar la aplicación.

El servidor se inicia en http://127.0.0.1:5000/ por defecto.

La API utiliza web scraping para obtener información, asegúrate de tener una conexión a internet estable.

El script puede ser detenido enviando una solicitud POST a /shutdown.