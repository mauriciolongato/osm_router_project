import time
from xlrd import open_workbook
from selenium import webdriver
import os
import json


def cria_url(origem_destino):
    x_ori = origem_destino[6]
    y_ori = origem_destino[5]
    x_des = origem_destino[8]
    y_des = origem_destino[7]
    #'http://router.project-osrm.org/viaroute?loc=-23.4243034,-46.4900888&loc=-18.4910633,-47.4063649&instructions=true&alt=false'
    #'http://router.project-osrm.org/viaroute?loc=-23.5324858,-46.79168&loc=-23.9608329,-46.3338889&instructions=true&alt=false'
    url = "http://router.project-osrm.org/viaroute?loc="+str(x_ori)+","+str(y_ori)+"&loc="+str(x_des)+","+str(y_des)+"&instructions=true&alt=false"
    return url

def readRows(sheet):
    # using list comprehension
    return [sheet.row_values(idx) for idx in range(sheet.nrows)]

# Abre a lista de origem destino
book = open_workbook('rotas_aero_parte_2.xlsx', on_demand=True)
# print("arquivo numero: ", n_arquivo, " - ", file)
data = []

driver = webdriver.Chrome('C:\\ChromeDrive\\chromedriver')

for name in book.sheet_names():
    sheet = book.sheet_by_name(name)
    rotas_raw = readRows(sheet)

cont = 0
for rota in rotas_raw[1:]:
    url = cria_url(rota)
    driver.get(url);
    html = driver.page_source
    print("/rota_"+str(rota[0])+'_'+str(cont))
    with open("./rotas_output"+"/rota_"+str(rota[0]), 'w') as outfile:
        json.dump(html, outfile)
    cont += 1
    time.sleep(0.95)

driver.quit()