from urllib.request import urlopen
import sqlite3 as sql
import pandas as pd
import time
import bs4
from selenium import webdriver

def cria_chave(row):
    chave = row['uf']+' '+row['municipio_nome']
    return chave

def get_url(row):
    url = 'http://nominatim.openstreetmap.org/search/__municipio__?format=json&addressdetails=1&limit=1&polygon_svg'
    string = url.replace("__municipio__",row['chave_osm'])
    return string.replace(" ","%20")

def fetch_url(url):
    html = urlopen(url)
    soup = bs4.BeautifulSoup(html, 'lxml')
    print(soup.prettify())
    print("'%s\' fetched in %ss" % (url, (time.time() - start)))
    return id, html

# Cria a coneccao com o banco de dados e obtem informacoes dos municipios
conn = sql.connect('20160706_Municipios.db')
municipios = conn.execute('''SELECT * FROM municipios WHERE uf = "MG" OR uf = "SP" OR uf = "ES" OR uf = "RJ";''')
cols = ['id_uf', 'uf', 'uf_nome', 'id_micro', 'micro_nome', 'id_municipio', 'municipio_nome']
municipios = pd.DataFrame.from_records(data = municipios.fetchall(), columns = cols)
municipios.to_csv('municipios_sudeste')
# Cria a chave de busca dos municipios para o osm
municipios['chave_osm'] = municipios.apply(lambda row:cria_chave(row), axis=1)
municipios['osm_url'] = municipios.apply(lambda row:get_url(row), axis=1)


#Obtem a informacao do osm referente a localizacao
#        Obtem as chaves de busca
ids = municipios['id_municipio'].values
urls = municipios['osm_url'].values

for url in urls:
    driver = webdriver.Chrome('C:\\ChromeDrive\\chromedriver')
    driver.get(url);
    html = driver.page_source
    print(html)
