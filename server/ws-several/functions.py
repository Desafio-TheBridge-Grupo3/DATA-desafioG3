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
    """
    Establishes a connection to the PostgreSQL database.

    The function uses the connection parameters (database name, user, password, host, and port)
    to create a connection string and then connects to the database using the psycopg2 library.

    Returns:
        psycopg2.extensions.connection: A connection to the PostgreSQL database.

    Raises:
        dict: An error dictionary containing an error message if the connection fails.
    """
    try:
        conn_string = f"dbname={DATABASE_NAME} user={USER} password={PASSWORD} host={HOST} port={PORT}"
        connection = psycopg2.connect(conn_string)
        
        return connection 
    except Exception as e:
        print({"Error": f"Error al conectarse a la base de datos: {e}"})
        return {"Error": f"Error al conectarse a la base de datos: {e}"}

def change_zones(zone):
    """
    Transforms a zone identifier to a simplified representation.

    The function takes a zone identifier as input and maps it to a simplified representation.
    It is specifically designed to handle cases where the input zone is "BALEARES" or "CANARIAS."
    If the input is "BALEARES," it returns "B." If the input is "CANARIAS," it returns "C."
    For any other input, it returns "P."

    Args:
        zone (str): The original zone identifier.

    Returns:
        str: The simplified representation of the zone ("B" for "BALEARES," "C" for "CANARIAS," or "P" for others).
    """
    if zone == "BALEARES":
      return "B"
    elif zone == "CANARIAS":
      return "C"
    else:
      return "P"
    
def remove_decimals(n):
    """
    Removes trailing ".0" or ",0" from a numeric string.

    The function takes a numeric string as input and checks if it ends with ".0" or ",0".
    If so, it removes the trailing part and returns the modified string. If not, it returns the
    original string unchanged.

    Args:
        n (str): The input numeric string.

    Returns:
        str: The modified numeric string with trailing ".0" or ",0" removed (if applicable).
    """
    if n.endswith('.0') or n.endswith(',0'):
        n = n.replace(",0", "")
        n = n.replace(".0", "")

    return str(n)

def clean_info(res):
    """
    Cleans and transforms information within a dictionary.

    The function takes a dictionary `res` as input and performs several cleaning and transformation operations:
    1. Transforms the 'zone' key using the 'change_zones' function.
    2. Converts the 'market' key to "F" if it is "FIJO," or "I" otherwise.
    3. Replaces '/' with '-' in the 'indexed_date' key.
    4. Removes trailing ".0" or ",0" from the 'fee' key using the 'remove_decimals' function.

    Args:
        res (dict): The input dictionary containing information to be cleaned.

    Returns:
        dict: The modified dictionary after cleaning and transformation operations.
    """
    res['zone'] = change_zones(res['zone'])
    res['market'] = "F" if res['market'] == "FIJO" else "I"
    res['indexed_date'] = res['indexed_date'].replace("/","-")
    res['fee'] = remove_decimals(res['fee'])

    return res

def con_filter_info(con, res):
    """
    Retrieves filtered information from the database based on the provided configuration.

    The function takes a database connection (`con`) and a configuration dictionary (`res`) as input.
    It performs cleaning on the configuration using the `clean_info` function, constructs SQL queries to
    retrieve information from two different tables (`cia_con_several` and `cia_pow_several`), and
    executes the queries using a cursor.

    Args:
        con (psycopg2.extensions.connection): The PostgreSQL database connection.
        res (dict): The configuration dictionary containing filtering criteria.

    Returns:
        dict: A dictionary containing the retrieved information or an error message.
            If successful, the dictionary structure includes 'con_prices' and 'pow_prices' keys
            with pricing information. If no results are found, these keys are set to None.
            If an error occurs during the process, the dictionary contains an 'error' key
            with the error message.
    """
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
        else:
            result_con = None

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
        else:
            result_pow = None
        result_info = {
            "con_prices": result_con,
            "pow_prices": result_pow
        }
    except Exception as e:
        result_info = {"error": str(e)}

    return result_info