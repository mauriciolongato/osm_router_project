import threading
import urllib2
import time
import json
import pandas as pd
import ast
import sqlite3 as sql
from multiprocessing.pool import ThreadPool

#cria a tabela
nome = '20160706_Municipios'
conn = sql.connect(nome+'.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS municipios;")
cur.execute('''CREATE TABLE municipios(
                     id_uf             INT
                    ,uf                VARCHAR(2)
                    ,uf_nome           VARCHAR(100)
                    ,id_micro          INT
                    ,micro_nome        VARCHAR(100)
                    ,id_municipio      INT
                    ,municipio_nome    VARCHAR(100)
    );''')

# obtem valores
address = 'C:\\Users\\mauricio.longato\\workspace\\OpenStreetMap_v3\\src\\arquivos_entrada\\municipios_mod.csv'
municipios = pd.read_csv(address, sep=';')

for row in municipios.values:
    cur.execute('''INSERT INTO municipios VALUES (?, ?, ?, ?, ?, ?, ?);''', (row[0] ,row[1] ,row[2] ,row[3] ,row[4] ,row[5] ,row[6]))

conn.commit()
conn.close()
