import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

def my_connection():

    print("Conexión exitosa!")
    try:
        conn_string = f"dbname={DATABASE_NAME} user={USER} password={PASSWORD} host={HOST} port={PORT}"
        connection = psycopg2.connect(conn_string)
        
        return connection 
    except Exception as e:
        print({"Error": f"Error al conectarse a la base de datos: {e}"})
        return {"Error": f"Error al conectarse a la base de datos: {e}"}

def change_zones(zone):
    if zone == "BALEARES":
      return "B"
    elif zone == "CANARIAS":
      return "C"
    else:
      return "P"
    
def remove_decimals(n):
    if n.endswith('.0') or n.endswith(',0'):
        n = n.replace(",0", "")
        n = n.replace(".0", "")

    return str(n)

def clean_info(res):
    res['zone'] = change_zones(res['zone'])
    res['market'] = "F" if res['market'] == "FIJO" else "I"
    res['indexed_date'] = res['indexed_date'].replace("/","-")
    res['fee'] = remove_decimals(res['fee'])

    return res

def con_filter_info(con, res):

    try:
        cursor = con.cursor()
        res_clean = clean_info(res)

        query = f"""
            SELECT 
                con_price_P1,
                con_price_P2,
                con_price_P3,
                con_price_P4,
                con_price_P5,
                con_price_P6
            FROM 
                cia_con_several
            WHERE
                cia = '{res_clean['cia']}'
            AND
                zone= '{res_clean['zone']}'
            AND
                rate= '{res_clean['rate']}'
            AND
                indexed_date= '{res_clean['indexed_date']}'
            AND
                fee= '{res_clean['fee']}'
            AND
                market= '{res_clean['market']}';

        """
        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
        if results:
            result_con = {
                    "con_price_P1": results[0][0],
                    "con_price_P2": results[0][1],
                    "con_price_P3": results[0][2],
                    "con_price_P4": results[0][3],
                    "con_price_P5": results[0][4],
                    "con_price_P6": results[0][5]
            }

        query = f"""
            SELECT 
                pow_price_P1,
                pow_price_P2,
                pow_price_P3,
                pow_price_P4,
                pow_price_P5,
                pow_price_P6
            FROM 
                cia_pow_several
            WHERE
                cia = '{res_clean['cia']}'
            AND
                zone= '{res_clean['zone']}'
            AND
                rate= '{res_clean['rate']}'
            AND
                product_cia= '{res_clean['product_cia']}'
            AND
                market= '{res_clean['market']}';
        """

        cursor.execute(query)
        results = cursor.fetchall()
        print(results)
        if results:
            result_pow = {
                    "pow_price_P1": results[0][0],
                    "pow_price_P2": results[0][1],
                    "pow_price_P3": results[0][2],
                    "pow_price_P4": results[0][3],
                    "pow_price_P5": results[0][4],
                    "pow_price_P6": results[0][5]
            }
        result_info = {
            "con_prices": result_con,
            "pow_prices": result_pow
        }
    except Exception as e:
        result_info = {"error": str(e)}

    return result_info