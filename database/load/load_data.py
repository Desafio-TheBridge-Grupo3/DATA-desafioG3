import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
PATH_XLSX = os.getenv("PATH_XLSX")
CONNECTION = os.getenv("CONNECTION")

def read_info_prices(path, header, sheet_name):
    """
    Reads information from an Excel file and returns a Pandas DataFrame.

    The function takes a file path (`path`), a header parameter (`header`), and a sheet name (`sheet_name`) as input.
    It uses the Pandas library to read the Excel file and return the data as a DataFrame.

    Args:
        path (str): The file path of the Excel file.
        header (int or list of int, default 0): Row(s) to use as the column names.
            Pass `None` if there are no column names.
        sheet_name (str, int, list, or None, default 0): The name or index of the sheet to read.
            If None, it reads all sheets.

    Returns:
        pandas.core.frame.DataFrame: A DataFrame containing the read data from the Excel file.
    """
    df = pd.read_excel(path, header=header, sheet_name=sheet_name)

    return df

def insert_several():
    """
    Reads and inserts information from Excel files into PostgreSQL database tables.

    The function reads two sheets ("FIJO" and "INDEXADO") from an Excel file located at PATH_XLSX.
    It performs various data cleaning and renaming operations on the DataFrames obtained from the sheets.
    The cleaned data is then merged, transformed, and inserted into two PostgreSQL tables ('cia_con_several'
    and 'cia_pow_several') using SQLAlchemy's create_engine and Pandas to_sql functions.

    The 'zone' and 'market' columns are standardized using the 'change_zones' and 'change_market' functions, respectively.

    Args:
        None

    Returns:
        None
    """
    try:
      df_fixed = read_info_prices(PATH_XLSX, 1, "FIJO")
      df_fixed.drop(columns="Unnamed: 0", inplace=True, axis=1)

      df_fixed.rename(columns={"sistema": "zone",
                              "cia": "cia",
                              "producto": "market",
                              "producto cia": "product_cia",
                              "tarifa": "rate",
                              "fee": "fee",
                              "P1":"con_price_p1",
                              "P2": "con_price_p2",
                              "P3": "con_price_p3",
                              "P4": "con_price_p4",
                              "P5": "con_price_p5",
                              "P6": "con_price_p6",
                              "P1.": "pow_price_p1",
                              "P2.": "pow_price_p2",
                              "P3.": "pow_price_p3",
                              "P4.": "pow_price_p4",
                              "P5.": "pow_price_p5",
                              "P6.": "pow_price_p6", 
                              }, inplace=True)
    
      df_indexed = read_info_prices(PATH_XLSX, 3, "INDEXADO")
      df_indexed_date = df_indexed.iloc[:,0:12]
      df_indexed_date.drop(columns="Unnamed: 0", inplace=True, axis=1)
      
      df_indexed_date.rename(columns={"SISTEMA": "zone",
                              "CIA": "cia",
                              "PRODUCTO": "market",
                              "PRODUCTO CIA": "product_name",
                              "TARIFA": "rate",
                              "FEE": "fee",
                              "MES": "indexed_date",
                              "P1.":"con_price_p1",
                              "P2.": "con_price_p2",
                              "P3.": "con_price_p3",
                              "P4.": "con_price_p4",
                              "P5": "con_price_p5",
                              "P6.": "con_price_p6"
                              }, inplace=True)
      df_indexed_date["market"] = "INDEXADO"
      df_indexed_date['indexed_date'] = df_indexed_date['indexed_date'].dt.strftime('%d-%m-%Y')

      df_con_sev = pd.concat([df_fixed, df_indexed_date])
      df_con_sev["zone"] = df_con_sev["zone"].apply(lambda zone: "B" if zone == "BALEARES" else ("C" if zone == "CANARIAS" else "P"))
      df_con_sev["market"] = df_con_sev["market"].apply(lambda m: "F" if m == "FIJO" else "I")
      df_con_sev.fillna(value=0)
      # Connection postgresql
      engine = create_engine(CONNECTION)
      df_con_sev.to_sql('cia_con_several', con=engine, index=False, if_exists='replace')

      # CIA POWER PRICES
      df_power = df_indexed.iloc[:,12:]
      df_power.drop(columns="Unnamed: 12", inplace=True, axis=1)
      df_power.dropna(inplace=True)
      df_power.rename(columns={"SISTEMA.1": "zone",
                              "CIA.1": "cia",
                              "PRODUCTO": "market",
                              "PRODUCTO CIA": "product_cia",
                              "TARIFA.1": "rate",
                              "P1":"pow_price_p1",
                              "P2": "pow_price_p2",
                              "P3": "pow_price_p3",
                              "P4": "pow_price_p4",
                              "P5.1": "pow_price_p5",
                              "P6": "pow_price_p6"
                              }, inplace=True)
      df_power["zone"] = df_power["zone"].apply(lambda zone: "B" if zone == "BALEARES" else ("C" if zone == "CANARIAS" else "P"))
      df_power["market"] = df_power["market"].apply(lambda m: "F" if m == "FIJO" else "I")
      df_power.fillna(value=0)
      df_power.to_sql('cia_pow_several', con=engine, index=False, if_exists='replace')

      engine.dispose()

      print("Se han insertado correctamente los datos en la base de datos")
    except Exception as e:
       print("Ha ocurrido un error al insertar los datos", str(e))

if __name__ == "__main__":
  insert_several()