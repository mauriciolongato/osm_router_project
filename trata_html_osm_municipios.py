import json
import bs4
import ast
import pandas as pd
from os import listdir
from os.path import isfile, join


# http://www.openstreetmap.org/relation/
address = './municipios_output'
onlyfiles = [f for f in listdir(address) if isfile(join(address, f))]

data_arq = []
for file in onlyfiles:
    with open(address+"/"+file) as json_data:
        d = json.load(json_data)
        json_data.close()
        html = d

    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        info_m = ast.literal_eval(soup.body.text)[0]
        header = ['id_ibge', 'osm_id', 'display_name', 'lon', 'lat']
        data = [file.split("_")[1], info_m['osm_id'], info_m['display_name'], info_m['lon'], info_m['lat']]
        data_pd = pd.DataFrame([data], columns=header)
        data_arq.append(data_pd)
        #print(file)
    except:
        print("deu ruim: ",file)

frame = pd.DataFrame()
frame = pd.concat(data_arq)
frame.to_csv("coordenadas_municipios.csv", sep="|", decimal=".")