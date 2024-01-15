import psycopg2
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from variables import CONNECTION, PATH_XLSX

def read_info_prices(path, header, sheet_name):
    df = pd.read_excel(path, header=header, sheet_name=sheet_name)

    return df

def change_zones(zone):
    if zone == "BALEARES":
      return "B"
    elif zone == "CANARIAS":
      return "C"
    else:
      return "P"
    
def change_market(m):
    if m == "FIJO":
        return "F"
    else:
        return "I"

def insert_several():
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
    df_con_sev["zone"] = df_con_sev["zone"].apply(change_zones)
    df_con_sev["market"] = df_con_sev["market"].apply(change_market)
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
    df_power["zone"] = df_power["zone"].apply(change_zones)
    df_power["market"] = df_power["market"].apply(change_market)
    df_power.fillna(value=0)
    df_power.to_sql('cia_pow_several', con=engine, index=False, if_exists='replace')

    engine.dispose()
insert_several()