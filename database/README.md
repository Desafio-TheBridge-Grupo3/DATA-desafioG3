# Database
## Diseño, creación y actualización de la base de datos

En esta carpeta se encuentran los archivos de trabajo relativos a la base de datos.

## Carpetas
- [`SQL`](/database/sql): Esquemas y querys de creación de la BBDD del proyecto.
- [`Load`](/database/load): Script de actualización de las tarifas en la BBDD.
- [`Notebooks`](/database/notebooks): Carpeta con notebooks de diferentes pruebas realizadas con la BBDD

# Importación y Carga de Datos a Base de Datos PostgreSQL

Este script de Python utiliza Pandas y SQLAlchemy para leer información desde archivos Excel y cargarla en tablas de una base de datos PostgreSQL.

## Requisitos

- Python 3.11
- Bibliotecas Python: pandas, sqlalchemy, dotenv

## Configuración

1. Instala las dependencias requeridas ejecutando:

   ```bash
   pip install pandas sqlalchemy python-dotenv
   ```
2. Crea un archivo .env en el mismo directorio que el script y define las siguientes variables:

    `PATH_XLSX=/ruta/a/tu/archivo.xlsx`

    `CONNECTION=postgresql://usuario:contraseña@localhost:5432/nombre_de_tu_base_de_datos`

3. Ejecuta el script para cargar los datos en la base de datos PostgreSQL:

    `python load_data.py`

## Detalles del Script

El script realiza las siguientes acciones:

- Lee datos desde dos hojas ("FIJO" e "INDEXADO") de un archivo Excel.
- Realiza operaciones de limpieza y renombrado de columnas en los DataFrames obtenidos.
- Combina y transforma los datos según las necesidades de las tablas 'cia_con_several' y 'cia_pow_several'.
- Conecta con la base de datos PostgreSQL utilizando SQLAlchemy y carga los datos en las tablas correspondientes.
