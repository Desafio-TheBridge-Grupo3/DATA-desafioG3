# Memoria técnica Data Science

## Análisis detallado del problema.

Se nos presenta la necesidad de crear una WebApp que substituya, y amplie, las funciones de una tabla de excel.
Las deficiencias de la manera de trabajo actual son varias:

+ Mala escalabilidad. La empresa ha comenzado a tener problemas a la hora de usarla en diferentes situaciones.
+ Poco control del trabajo realizado. Enfarragosa manera de guardar historiales.
+ Exceso de trabajo por parte del asesor a la hora de introducir datos

## Propuesta de solución tecnológica

La tarea de suplantar el trabajo realizado por una hoja excel con una WebApp plantea la oportunidad de usar una BBDD relacional, que acabe con los problemas de escalabilidad y registro de históricos. A ello añadimos la posibilidad de obtener datos de forma automatizada, aliviando la carga de trabajo del asesor.

+ BBDD SQL Relacional (PostgreSQL)
+ Webscrapping (Selenium)
+ Scrapeo de PDF e imágenes (OpenCV, PyMuPDF, Regex)


# BBDD SQL

Una vez analizadas las necesidades de la WebApp para solucionar los problemas actuales, se diseña la BBDD que cumpla las funciones necesarias para el proyecto.
Se trata de una BBDD PostreSQL 15.0, preparada para alojarse en la nube Azure. Tiene 12 entidades y 5 relaciones. [Link a la query de creación](database\sql\create_tables.sql)
### Estructura

[![!Estructura](/aux_temp/Esquema.png)](https://www.canva.com/design/DAF5e_nv_Bk/PNXGmx8l0Xajcoh2LPONFQ/edit?utm_content=DAF5e_nv_Bk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
<span style="font-size: small; color: gray;">Click en la imágen para ampliar</span>

### Relación
[![Relación](/aux_temp/Diagrama.png)](https://www.canva.com/design/DAFy6dl3Pe4/yYekcQiBpDDn7MCyx_-qiw/edit?utm_content=DAFy6dl3Pe4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
<span style="font-size: small; color: gray;">Click en la imágen para ampliar</span>

# Automatización de extracción de Datos.

El flujo del trabajo manual del asesor actual tiene dos tareas penosas en tiempo que son candidatas a ser substituidas por automatismos.
Se trata, por un lado,de la obtención de datos desde una intranet a la que se accede vía web, y con un código "CUPs" se extraen datos. Y por otro lado, la lectura personal de facturas para obtener datos de consumo y precios.

## WebScraping

Mediante el uso de la librería Selenium, creamos un script que accede vía web a la información requerida.

## Scrapeo de PDF e Imagen





BBDD
Automatismos de extracción de datos
modelo de predicción 
dashboard