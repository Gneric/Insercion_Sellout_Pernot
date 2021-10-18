from src.utils.connection import *
from os import getcwd, scandir, remove
from os.path import join

import pandas as pd
import sqlalchemy as sa
import pyodbc
import urllib


data_path = join(getcwd(),'src','data')

def cleanDataFolder():
    for file in scandir(data_path):
        remove(file)

def truncateTable(table_name):
    try:
        cn = pernod_conn
        conn_string = f"DRIVER='{cn['driver']}';SERVER='{cn['server']}';DATABASE='{cn['db']}';UID='{cn['uid']}';PWD='{cn['pwd']}'"
        print(conn_string)
        conn = pyodbc.connect(conn_string)
        with conn:
            cursor = conn.cursor()
            query = f"TRUNCATE TABLE {table_name}"
            print('Truncando tabla')
            cursor.execute(query)
            conn.commit()
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(sqlstate)

def loadFile(table_name, file):
    try:
        cn = pernod_conn
        conn_string = f"DRIVER='{cn['driver']}';SERVER='{cn['server']}';DATABASE='{cn['db']}';UID='{cn['uid']}';PWD='{cn['pwd']}'"
        print(conn_string)
        connection_uri = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(conn_string)}"
        engine = sa.create_engine(connection_uri, fast_executemany=True)
        file_path = join(data_path, file)
        xlsx = pd.read_excel(file_path)
        xlsx.columns = table_info
        df = xlsx.fillna('')
        print('insertando Datos')
        df.to_sql(table_name,engine,if_exists='append',index=False)
        print(f'Data ingresada a tabla : {table_name}')
    except:
        print(f'Error insertando datos a tabla {table_name}')

    

