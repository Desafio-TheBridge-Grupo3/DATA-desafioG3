# API ws-several

Esta API ws-several proporciona un servicio para filtrar información de una base de datos basándose en criterios proporcionados en una configuración JSON.

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

El servidor se iniciará en http://127.0.0.1:5002/

## Endpoints

- Endpoint: http://127.0.0.1:5001/filter_several
- Método: GET 
- Descripción: Filtra la información de la base de datos según los criterios proporcionados en una configuración JSON.
- Parámetros de Entrada: Se espera un objeto JSON con campos específicos según el esquema definido.
    - Ejemplo JSON : 
        ```bash
        {
            "cia": "XXXX",
            "zone": "X",
            "rate": "XXXXX",
            "indexed_date": "XX-XX-XXXX",
            "fee": "XXXXXX",
            "product_cia": "XXXXXX",
            "market": "X" 
        }
        ```
- Respuesta:
    - Exitosa:
        ```bash
            {
            "response": {
                "con_prices": {
                    "con_price_P1": X.XXXXXX,
                    "con_price_P2": X.XXXXXX,
                    "con_price_P3": X.XXXXXX,
                    "con_price_P4": X.XXXXXX,
                    "con_price_P5": X.XXXXXX,
                    "con_price_P6": X.XXXXXX
                },
                "pow_prices": {
                    "pow_price_P1": X.XXXXXX,
                    "pow_price_P2": X.XXXXXX,
                    "pow_price_P3": X.XXXXXX,
                    "pow_price_P4": X.XXXXXX,
                    "pow_price_P5": X.XXXXXX,
                    "pow_price_P6": X.XXXXXX
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

El servidor se inicia en http://0.0.0.0:5002/ por defecto.

La API utiliza CORS para permitir solicitudes desde cualquier origen ('*').

Ajusta los parámetros según las necesidades específicas de tu aplicación.