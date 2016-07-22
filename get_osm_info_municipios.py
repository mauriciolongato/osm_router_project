import threading
import urllib2
import sqlite3 as sql
import pandas as pd
import time
from multiprocessing.pool import ThreadPool

def cria_chave(row):
    chave = row['uf']+' '+row['municipio_nome']
    return chave

def get_url(row):
    url = 'http://nominatim.openstreetmap.org/search/__municipio__?format=json&addressdetails=1&limit=1&polygon_svg'
    string = url.replace("__municipio__",row['chave_osm'])
    return string.replace(" ","%20")

def fetch_url(url, id):
    urlHandler = urllib2.urlopen(url)
    html = urlHandler.read()
    print "'%s\' fetched in %ss" % (url, (time.time() - start))
    return id, html

#Cria a coneccao com o banco de dados e obtem informacoes dos municipios
conn = sql.connect('20160706_Municipios.db')
municipios = conn.execute('''SELECT * FROM municipios;''')
cols = ['id_uf', 'uf', 'uf_nome', 'id_micro', 'micro_nome', 'id_municipio', 'municipio_nome']
municipios = pd.DataFrame.from_records(data = municipios.fetchall(), columns = cols)

#Cria a chave de busca dos municipios para o osm
municipios['chave_osm'] = municipios.apply(lambda row:cria_chave(row),axis=1)
municipios['osm_url']   = municipios.apply(lambda row:get_url(row),axis=1)


#Obtem a informacao do osm referente a localizacao
#        Obtem as chaves de busca
ids  = municipios['id_municipio'].values
urls = municipios['osm_url'].values

#        Executa as threads
start_main = time.time()
pool = ThreadPool(processes=5)

async_result = [pool.apply_async(fetch_url, (url,id)) for url, id in zip(urls, ids)] # tuple of args for foo
print async_result[0][0].get()
results = [result.get() for result in async_result]

cols = ['id_municipio', 'position_info']
thread_result = pd.DataFrame.from_records(data = results, columns = cols)
#rotas_rodo = rotas_rodo.merge(thread_result, left_on='thread_id', right_on=0, how='left')
municipios =  municipios.merge(thread_result, left_on='id_municipio', right_on='id_municipio', how='left')
print municipios
